from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import User
from .utils import send_message
from random import randint


@receiver(post_save, sender=User)
def send_email_for_user(sender, instance, created, **kwargs):
    if created:
        message = ''.join([str(randint(1, 10)) for _ in range(4)])
        send_message(instance.email, message)
