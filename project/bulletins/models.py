from parler.models import TranslatableModel, TranslatedFields
from tinymce.models import HTMLField
from django.db import models


class Bulletins(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=25),
        description=HTMLField(verbose_name='Описание'),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Бюллетень'
        verbose_name_plural = 'Бюллетени'

    def __str__(self):
        return self.title
