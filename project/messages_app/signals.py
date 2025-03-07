from django.db.models.signals import pre_save, post_save, Signal
from django.dispatch import receiver
from .models import Messages
import requests
import os

create_user_signal = Signal()

@receiver(post_save, sender=Messages)
def telegram_message_send(sender, instance, created, **kwargs):
    if created:
        message = f'{instance.name} только что отправила сообщение об инциденте'
        response = requests.get(
            url=f'{os.getenv('TELEGRAM_API')}/sendMessage?chat_id={os.getenv('TELEGRAM_CHAT_ID')}&text={message}')