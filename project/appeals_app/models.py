from django.db import models

from accounts_app.models import Organization


class Appeal(models.Model):
    message = models.TextField(null=False, blank=False, verbose_name='Сообщения')
    full_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='ФИО')
    email = models.EmailField(null=False, blank=False, verbose_name='Email')
    phone_number = models.CharField(max_length=300, null=False, blank=False, verbose_name='Номер телефона')
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE, related_name='appeal', null=True,
                                     blank=True, verbose_name='Организация')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата обращения')

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        db_table = 'appeals'
        verbose_name = 'Обращения'
        verbose_name_plural = 'Обращения'
