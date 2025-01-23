from django.urls import path

from .views import send_messages_post, MessageListOnUser

urlpatterns = [
    path('send/', send_messages_post, name='send_message'),
    path('list/', MessageListOnUser.as_view(), name='message_list'),
]