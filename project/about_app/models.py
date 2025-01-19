from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from tinymce.models import HTMLField


class About(TranslatableModel):
    translations = TranslatedFields(
        description=HTMLField(verbose_name='Подробное описание')
    )

    class Meta:
        db_table = 'About'
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'

    def __str__(self):
        return f'{self.pk}'


class CenterTasks(TranslatableModel):
    translations = TranslatedFields(
        description=models.TextField(verbose_name='Подробное описание')
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        db_table = 'CenterTasks'
        verbose_name = 'Задачи центра'
        verbose_name_plural = 'Задачи центра'

    def __str__(self):
        return f'{self.pk}'
