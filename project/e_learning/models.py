from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class ELearning(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, blank=False, null=False, verbose_name='Наименование')
    )
    link = models.URLField(max_length=150, verbose_name='Ссылка')

    class Meta:
        db_table = 'ELearning'
        verbose_name = 'E-Learning'
        verbose_name_plural = 'E-Learning'

    def __str__(self):
        return f'{self.name}'
