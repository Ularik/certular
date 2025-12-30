from django.utils.translation import activate
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_language = request.GET.get('language')
            print(user_language)
            activate(user_language)
        else:
            activate(settings.LANGUAGE_CODE)
        response = self.get_response(request)
        return response


class RateLimitMiddleware:
    RATE_LIMIT = 40  # max запросов
    WINDOW = 60      # секунд = 1 минута

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        key = f"rate-limit:{ip}"

        # количество запросов
        req_count = cache.get(key, 0)

        if req_count >= self.RATE_LIMIT:
            return JsonResponse(
                {"detail": "Too many requests, slow down."},
                status=429
            )

        # увеличиваем счётчик
        if req_count == 0:
            cache.set(key, 1, timeout=self.WINDOW)
        else:
            cache.incr(key)

        return self.get_response(request)

    def get_client_ip(self, request):
        xfwd = request.META.get("HTTP_X_FORWARDED_FOR")
        if xfwd:
            return xfwd.split(",")[0]
        return request.META.get("REMOTE_ADDR")
