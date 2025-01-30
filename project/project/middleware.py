from django.utils.translation import activate
from django.conf import settings


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