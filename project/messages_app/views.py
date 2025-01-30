from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView
from accounts_app.models import User
from .models import Messages
from django.utils.translation import get_language
import re


pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,5}$"

def send_messages_post(request, *args, **kwargs):

    if request.method == 'POST':
        request_body = request.POST
        if request.FILES:
            file_message = request.FILES.get('file')
        else:
            file_message = request_body['file']

        if request_body['description'] == '':
            form_desc_invalid = ''
            if get_language() == 'en':
                form_desc_invalid = {"error": "Fill in all the fields"}
            elif get_language() == 'ru':
                form_desc_invalid = {"error": "Заполните все поля"}
            elif get_language() == 'ky':
                form_desc_invalid = {'error': 'Бардык талааларды толтуруңуз'}
            return JsonResponse(form_desc_invalid, status=400)

        if not request.user.is_authenticated:
            print('User not auth')

            if request_body['phone_number'] == '':
                form_desc_invalid = ''
                if get_language() == 'en':
                    form_desc_invalid = {"error": "Fill in all the fields"}
                elif get_language() == 'ru':
                    form_desc_invalid = {"error": "Заполните все поля"}
                elif get_language() == 'ky':
                    form_desc_invalid = {'error': 'Бардык талааларды толтуруңуз'}
                return JsonResponse(form_desc_invalid, status=400)

            if re.match(pattern, request_body['email']) is None:
                form_email_invalid = {"errors": "Введите правильную почту"}
                if get_language() == 'en':
                    form_email_invalid = {"errors": "Enter correct e-mail"}
                elif get_language() == 'ru':
                    form_email_invalid = {"errors": "Введите правильную почту"}
                elif get_language() == 'kg':
                    form_email_invalid = {'errors': 'Туура почтаны киргизиңиз'}
                return JsonResponse(form_email_invalid, status=400)

            Messages.objects.create(
                email=request_body['email'],
                phone_number=request_body['phone_number'],
                description=request_body['description'],
                file=file_message,
                host_ip=request_body['host_ip'],
                domain_name=request_body['domain_name'],
                hash=request_body['hash']
            )
            return JsonResponse({"success": "Successfully messages"})
        else:
            print('Success!')
            user = request.user
            Messages.objects.create(
                user=user,
                description=request_body['description'],
                file=file_message,
                host_ip=request_body['host_ip'],
                domain_name=request_body['domain_name'],
                hash=request_body['hash']
            )

        return JsonResponse({"success": "Successfully messages"})


class MessageListOnUser(LoginRequiredMixin, ListView):
    model = Messages
    template_name = 'messages/message_list.html'
    context_object_name = 'messages'
    login_url = 'forbidden'

    def get_queryset(self):
        queryset = Messages.objects.filter(user=self.request.user)
        # print(queryset)
        return queryset
