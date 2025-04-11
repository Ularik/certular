from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Contacts(TranslatableModel):
    translations = TranslatedFields(
        address=models.CharField(max_length=255, verbose_name='Адрес', null=True)
    )

    phone = models.CharField(max_length=255, verbose_name='Телефон', null=True, blank=True)
    email = models.EmailField(verbose_name='email', null=True)

    class Meta:
        db_table = 'Contacts'
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"Контакты"
