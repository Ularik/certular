from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.utils.translation import get_language
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
import datetime
import json
from django.views import View
from .models import User, Organization
import re
import logging
from django.core.cache import cache
from .signals import create_user_signal


logger = logging.getLogger(__name__)


@login_required
def my_view(request):
    ...


@login_required(login_url='/accounts/login/')
def logout_view(request):
    logout(request)
    return redirect('main_app:index')


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

        logger.info(f'{user.first_name} из {user.organization} вошел в систему в '
               f'{datetime.datetime.now().strftime("%d-%m-%Y - %H:%M")}')

        return JsonResponse({'success': "you in authenticated"}, status=200)
    else:
        error_message = {'error': "Неправильно указана почта или пароль"}
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


class RegistrationAPIView(View):

    def post(self, request, *args, **kwargs):
        request_body = json.loads(request.body)

        organization = Organization.objects.filter(id=int(request_body['organization'])).first()
        request_body['organization'] = organization

        if User.objects.filter(email=request_body['email']).exists():
            error_email = {"error": "Эта почта уже зарегистрирована"}
            if get_language() == 'en':
                error_email = {"error": "This email is all ready registered"}
            elif get_language() == 'ru':
                error_email = {"error": "Эта почта уже зарегистрирована"}
            elif get_language() == 'ky':
                error_email = {'error': 'Бул кат мурунтан эле катталган'}
            return JsonResponse(error_email)

        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,5}$"

        if re.match(pattern, request_body['email']) is None:
            form_email_invalid = {"error": "Введите правильную почту"}
            if get_language() == 'en':
                form_email_invalid = {"error": "Enter correct e-mail"}
            elif get_language() == 'ru':
                form_email_invalid = {"error": "Введите правильную почту"}
            elif get_language() == 'ky':
                form_email_invalid = {'error': 'Туура почтаны киргизиңиз'}
            return JsonResponse(form_email_invalid, status=400)
        try:
            user = User(
                first_name=request_body['first_name'],
                last_name=request_body['last_name'],
                patronymic=request_body['patronymic'],
                position=request_body['position'],
                organization=request_body['organization'],
                email=request_body['email'],
                number=request_body['number']
            )
            cache.set(request_body['number'], user)
            request.session['number'] = request_body['number']
            request.session['email'] = request_body['email']
            create_user_signal.send(sender=User, instance=user)
            return JsonResponse({"success": "Successfully registration"})
        except(BaseException) as e:
            print('Ошибка!!!')
            print(e)
            some_wrong = {'error': 'Заполните все поля'}
            if get_language() == 'en':
                some_wrong = {"error": "Fill in all the fields"}
            elif get_language() == 'ru':
                some_wrong = {'error': 'Заполните все поля'}
            elif get_language() == 'ky':
                some_wrong = {'error': 'Бардык талааларды толтуруңуз'}
            return JsonResponse(some_wrong, status=400)


def check_registration(request):
    if request.method == 'POST':
        email = request.session['email']
        number = request.session['number']

        code = cache.get(email)
        user = cache.get(number)

        data = json.loads(request.body)
        code2 = data.get('code')

        if code == code2:
            cache.delete(email)
            request.session.pop('email')
            user.save()
            return JsonResponse({'success': 'True'})
        else:
            return JsonResponse({'error': 'False'})


def answer_after_reg(request):
    return render(request, 'accounts/check_registration.html')