from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import requests


def send_message(account_email, message):
    from_name = 'КЦОКБ:'
    from_email = settings.EMAIL_HOST_USER
    to = account_email
    try:
        print('Отправляем сообщение с кодом')
        send_mail(from_name, message, from_email, [to])
    except BadHeaderError:
        print('bad email')


def check_recaptcha(recaptcha_response):

    if not recaptcha_response:
        print('Отсутствует токен из формочки')
        return {"error": "reCAPTCHA токен отсутствует"}

    # Запрос к Google API для проверки
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        "secret": settings.RECAPTCHA_PRIVATE_KEY,
        "response": recaptcha_response
    }
    print('Далее секрет кей и токен из формочки:')
    print(payload)
    print()
    response = requests.post(url, data=payload)
    result = response.json()

    # Проверка результата
    if not result.get("success"):
        error_codes = result.get("error-codes", [])
        print(result)
        return {"error": "Ошибка reCAPTCHA", "error_codes": error_codes}
    else:
        score = result.get("score")  # Оценка от 0.0 до 1.0
        action = result.get("action")  # Проверяем, что action совпадает
        print(action, score)

        # Пример порога: если score >= 0.5, считаем, что это человек
        if not (score >= 0.5 and (action == "submit" or action == "register")):
            return {"error": "Низкий score, возможно, вы бот", "score": score}

    return {'success': True}
