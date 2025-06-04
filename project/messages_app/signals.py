from django.db.models.signals import pre_save, post_save, Signal
from django.dispatch import receiver
from accounts_app.utils import send_message

response_to_report = Signal()

@receiver(response_to_report)
def send_response_to_sender(sender, message, **kwargs):
    send_message(sender.email, message)