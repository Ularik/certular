from django.urls import path

from .views import send_messages_post, MessageListOnUser, verify_captcha

app_name = 'messages'

urlpatterns = [
    path('send/', send_messages_post, name='send_message'),
    path('list/', MessageListOnUser.as_view(), name='message_list'),
    path('verify-captcha/', verify_captcha, name='captcha'),
]