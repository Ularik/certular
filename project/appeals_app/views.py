import json
import re

from django.http import JsonResponse
from django.utils.translation import get_language
from .forms import AddAppealForm


def appeals_post(request, *args, **kwargs):
    if request.method == 'POST':
        request_body = json.loads(request.body)

        form = AddAppealForm(request_body)
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,5}$"

        if re.match(pattern, request_body['email']) is None:
            form_email_invalid = {"errors": "Введите правильную почту"}
            if get_language() == 'en':
                form_email_invalid = {"errors": "Enter correct e-mail"}
            elif get_language() == 'ru':
                form_email_invalid = {"errors": "Введите правильную почту"}
            elif get_language() == 'kg':
                form_email_invalid = {'errors': 'Туура почтаны киргизиңиз'}
            return JsonResponse(form_email_invalid, status=400)

        if form.is_valid():
            print('Сохраняем  в модульку')
            apeal = form.save()
            print(apeal)
            return JsonResponse({"success": "Successfully registration"})
        else:
            print('Не удалось сохранить')
            form_is_invalid = {"errors": "Заполните все поля"}
            if get_language() == 'en':
                form_is_invalid = {"errors": "Fill in all the fields"}
            elif get_language() == 'ru':
                form_is_invalid = {"errors": "Заполните все поля"}
            elif get_language() == 'kg':
                form_is_invalid = {'errors': 'Бардык талааларды толтуруңуз'}
            return JsonResponse(form_is_invalid, status=403)
