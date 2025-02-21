from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from random import randint
import requests
from django.core.cache import cache


def send_message(account_email, message):
    from_name = 'КЦОКБ:'
    from_email = settings.EMAIL_HOST_USER
    to = account_email
    try:
        send_mail(from_name, message, from_email, [to])
    except BadHeaderError:
        print('bad email')

def send_email_for_user(email):
    message = ''.join([str(randint(1, 10)) for _ in range(4)])
    cache.set(email, message, 60 * 3)

    send_message(email, message)
    response = requests.get(
        url=f'https://api.telegram.org/7700044687:AAH61M2DCeM-Gg5xCytggZl-IYme92TSvd4/sendMessage?chat_id=7700044687Зарегистрировался новый пользователь')