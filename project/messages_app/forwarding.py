"""Пересылка заявок об инцидентах на внешний адрес (settings.MESSAGE_SEND_ADDRESS)."""
import logging
import os
import threading

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

FORWARD_TIMEOUT = 15  # секунд


def build_payload(message):
    """Поля заявки, отправляемые во внешнюю систему."""
    user = message.user
    return {
        'id': str(message.pk),
        'email': message.email or (user.email if user else '') or '',
        'full_name': message.name or '',
        'phone_number': message.phone_number or '',
        'description': message.description or '',
        'host_ip': message.host_ip or '',
        'domain_name': message.domain_name or '',
        'hash': message.hash or '',
        'user_id': str(user.pk) if user else '',
        'organization': str(user.organization) if user and user.organization_id else '',
        'created_at': message.created_at.isoformat() if message.created_at else '',
    }


def send_message_to_address(message, address):
    """Синхронно отправляет заявку POST-запросом (multipart/form-data, файл в поле `file`)."""
    data = build_payload(message)
    try:
        if message.file:
            with message.file.open('rb') as f:
                files = {'file': (os.path.basename(message.file.name), f)}
                response = requests.post(address, data=data, files=files, timeout=FORWARD_TIMEOUT)
        else:
            response = requests.post(address, data=data, timeout=FORWARD_TIMEOUT)
        response.raise_for_status()
    except Exception:
        logger.exception('Не удалось переслать заявку об инциденте id=%s на %s', message.pk, address)
        return False
    logger.info('Заявка об инциденте id=%s переслана на %s (HTTP %s)', message.pk, address, response.status_code)
    return True


def forward_message(message):
    """Если задан MESSAGE_SEND_ADDRESS, пересылает заявку в фоновом потоке, не задерживая ответ пользователю."""
    address = getattr(settings, 'MESSAGE_SEND_ADDRESS', '')
    if not address:
        return
    threading.Thread(target=send_message_to_address, args=(message, address), daemon=True).start()
