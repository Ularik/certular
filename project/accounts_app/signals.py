from django.db.models.signals import pre_save, post_save, Signal
from django.dispatch import receiver
from .models import User
from .utils import send_message
from random import randint
from django.core.cache import cache
import requests
import os

create_user_signal = Signal()


@receiver(create_user_signal)
def send_email_for_user(sender, instance, **kwargs):
    message = ''.join([str(randint(1, 10)) for _ in range(4)])
    print(message)
    cache.set(instance.email, message, 60 * 3)

    send_message(instance.email, message)


@receiver(post_save, sender=User)
def telegram_message(sender, instance, created, **kwargs):
    if created:
        message = f'Пользователь: {instance.email} только что отправил запрос на создание'
        response = requests.get(
            url=f'{os.getenv('TELEGRAM_API')}/sendMessage?chat_id={os.getenv('TELEGRAM_CHAT_ID')}&text={message}')


