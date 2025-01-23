import json
import uuid
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView
from accounts_app.models import User
from .models import Messages
from django.utils.translation import get_language


# @csrf_exempt
def send_messages_post(request, *args, **kwargs):

    if request.method == 'POST':
        request_body = json.loads(request.body)
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
            JsonResponse({'error': 'no auth'}, status=400)
        else:
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
