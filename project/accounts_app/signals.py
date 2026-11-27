from django.db.models.signals import pre_save, post_save, Signal
from django.dispatch import receiver
from .models import User
from .utils import send_message
from random import randint
from django.core.cache import cache
import logging
import os
import requests

logger = logging.getLogger(__name__)

create_user_signal = Signal()


@receiver(create_user_signal)
def send_email_for_user(sender, instance, **kwargs):
    message = ''.join([str(randint(1, 10)) for _ in range(4)])
    print(message)
    cache.set(instance.email, message, 60 * 3)

    send_message(instance.email, message)


@receiver(post_save, sender=User)
def telegram_message(sender, instance, created, **kwargs):
    if not created:
        return
    api = os.getenv('TELEGRAM_API')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not api or not chat_id:
        return
    message = f'Пользователь: {instance.email} только что отправил запрос на создание'
    # Сбой Telegram не должен ломать создание пользователя (в т.ч. из админки)
    try:
        requests.get(f'{api}/sendMessage', params={'chat_id': chat_id, 'text': message}, timeout=5)
    except requests.RequestException as e:
        logger.warning('Не удалось отправить уведомление в Telegram: %s', e)
