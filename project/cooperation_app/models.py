from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django_resized import ResizedImageField


class Cooperation(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, blank=False, null=False, verbose_name='Наименование'),
        image=ResizedImageField(quality=80, force_format='WEBP',
                                upload_to='cooperation', null=True, blank=False, verbose_name='Файл')
    )
    link = models.URLField(max_length=150, verbose_name='Ссылка')

    # image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], quality=80, force_format='WEBP',
    #                           upload_to='cooperation', null=False, blank=False, verbose_name='Файл')

    # created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        db_table = 'Cooperation'
        verbose_name = 'Сотрудничество'
        verbose_name_plural = 'Сотрудничество'

    def __str__(self):
        return f'{self.name}'
