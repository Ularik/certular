from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import get_language
import json


@login_required
def my_view(request):
    ...


def logout_view(request):
    logout(request)


def login_view(request):
    request_body = json.loads(request.body)
    user = authenticate(username=request_body['username'], password=request_body['password'])
    remember_me = ''
    if 'remember_me' in request_body:
        remember_me = request_body['remember_me']

    if user:
        if remember_me == 'on':
            request.session.set_expiry(1209600)  # if remember me is
        else:
            request.session.set_expiry(0)
        login(request, user)
        return JsonResponse({'success': "you in authenticated"}, status=200)
    else:
        error_message = ''
        if get_language() == 'en':
            error_message = {'error': "The email address or password is incorrect"}
        if get_language() == 'ru':
            error_message = {'error': "Неправильно указана почта или пароль"}
        if get_language() == 'ky':
            error_message = {'error': "Электрондук почта дареги же сыр сөз туура эмес"}
        return JsonResponse(error_message, status=401)


def my_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        ...