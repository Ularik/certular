from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields
from tinymce.models import HTMLField


class CyberSecurity(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name='Название'),
        description=HTMLField(verbose_name='Подробное описание'),
    )
    image = models.ImageField(upload_to='cyber_security', null=False, blank=False, verbose_name='Картинка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        db_table = 'CyberSecurity'
        verbose_name = 'Кибербезопасность'
        verbose_name_plural = 'Кибербезопасность'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('cyber_security:cyber_security', kwargs={'pk': self.pk})


class CyberIncident(TranslatableModel):
    translations = TranslatedFields(
        description=HTMLField(verbose_name='Описание'),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Инцидент кибербезопасности'
        verbose_name_plural = 'Инциденты кибербезопаснсти'

    def __str__(self):
        return f'Cyber incident'