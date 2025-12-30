from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


def send_message(account_email, message):
    from_name = 'КЦОКБ:'
    from_email = settings.EMAIL_HOST_USER
    to = account_email
    try:
        print('Отправляем сообщение')
        send_mail(from_name, message, from_email, [to])
        print('сообщение отправлено')
    except BadHeaderError:
        print('bad email')

