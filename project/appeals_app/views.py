import json
import re

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from .forms import AddAppealForm


def appeals_post(request, *args, **kwargs):
    # print('zdesssss')
    if request.method == 'POST':
        # print(form)
        # print(request.body)
        # print(type(json.loads(request.body)))
        request_body = json.loads(request.body)
        # print('zdessssss2222222 apeaaaaaallllllssssssssss')
        # print(request_body)
        # if request_body['number'] == "" or len(request_body['number']) != 12:
        #     return JsonResponse({"error": "This field is required"})
        # if User.objects.filter(email=request_body['email']).exists():
        #     return JsonResponse({"error": "This email is all ready"})
        # print(request_body['first_name'])
        form = AddAppealForm(request_body)
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,5}$"

        if re.match(pattern, request_body['email']) is None:
            print('email zdessss')
            form_email_invalid = ''
            if get_language() == 'en':
                form_email_invalid = {"errors": "Enter correct e-mail"}
            elif get_language() == 'ru':
                form_email_invalid = {"errors": "Введите правильную почту"}
            elif get_language() == 'ky':
                form_email_invalid = {'errors': 'Туура почтаны киргизиңиз'}
            return JsonResponse(form_email_invalid, status=400)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            # print('zdesss')
            # kwargs = {'slug': self.slug}
            return JsonResponse({"success": "Successfully registration"})
        else:
            form_is_invalid = ''
            if get_language() == 'en':
                form_is_invalid = {"errors": "Fill in all the fields"}
            elif get_language() == 'ru':
                form_is_invalid = {"errors": "Заполните все поля"}
            elif get_language() == 'ky':
                form_is_invalid = {'errors': 'Бардык талааларды толтуруңуз'}
            return JsonResponse(form_is_invalid, status=403)
