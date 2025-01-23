from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from tinymce.models import HTMLField


class Legislation(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, blank=False, null=False, verbose_name='Наименование'),
        description=HTMLField(blank=False, null=False, verbose_name='Полное описание'),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        db_table = 'Legislation'
        verbose_name = 'Законодательство'
        verbose_name_plural = 'Законодательство'

    def __str__(self):
        return f'{self.name}'


class Regulations(TranslatableModel):
    translations = TranslatedFields(
        description=models.TextField(blank=False, null=False, verbose_name='Описание'),
    )
    link = models.URLField(max_length=255, blank=False, null=True, verbose_name='Ссылка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        db_table = 'Regulations'
        verbose_name = 'Нормативно правовые акты'
        verbose_name_plural = 'Нормативно правовые акты'

    def __str__(self):
        return f'{self.link}'
