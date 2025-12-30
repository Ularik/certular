from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils import content_file_name

CHOICES = [('no read', _('Не прочитан')), ('completed', _('Завершен')), ('had read', _('Прочитан'))]


class Messages(models.Model):
    description = models.TextField(blank=True, null=True, verbose_name='Описание сообщения')
    user = models.ForeignKey('accounts_app.User', blank=True, null=True, on_delete=models.CASCADE,
                             related_name='messages', verbose_name='Пользователь')
    name = models.CharField(max_length=150, verbose_name='ФИО')
    file = models.FileField(upload_to=content_file_name('Messages'), null=True, blank=True, verbose_name='Файл')
    email = models.EmailField(null=False, blank=False, verbose_name='Email')
    phone_number = models.CharField(max_length=19, blank=True, null=True, verbose_name='Мобильный номер',
                                    validators=[MaxLengthValidator])
    host_ip = models.TextField(blank=True, null=True, verbose_name='IP')
    domain_name = models.TextField(blank=True, null=True, verbose_name='Domain Name')
    hash = models.TextField(blank=True, null=True, verbose_name='Hash')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')


    class Meta:
        db_table = 'Messages'
        verbose_name = 'Сообщение об инциденте'
        verbose_name_plural = 'Сообщения об инцидентах'
