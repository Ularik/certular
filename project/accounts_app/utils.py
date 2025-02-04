from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.cache import cache


def send_message(account_email, message):
    from_name = 'КЦОКБ:'
    from_email = settings.EMAIL_HOST_USER
    print(f'code: {message}')
    cache.set("account_email", message, 60 * 3)
    to = account_email
    try:
        send_mail(from_name, message, from_email, [to])
    except BadHeaderError:
        print('bad email')
