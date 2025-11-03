from django.db import models
from parler.models import TranslatableModel, TranslatedFields
import datetime
from news_app.models import NotificationNpa


def content_file_name(directory):
    # file will be uploaded to MEDIA_ROOT/customers/yearmonthday/<filename>
    today = datetime.date.today().strftime("%Y-%m-%d")
    return "{directory}/{date}".format(directory=directory, date=today)


class CryptoProvider(TranslatableModel):
    title = models.CharField(max_length=70, null=True, blank=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=200, blank=False, null=False, verbose_name='Наименование'),
        description=models.TextField(blank=False, null=False, verbose_name='Описание'),
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    )
    crypto_npa = models.ManyToManyField(NotificationNpa, null=True, blank=True)
    npa_links = models.ManyToManyField('NpaLinks', null=True, blank=True)

    class Meta:
        db_table = 'CryptoProvider'
        verbose_name = 'СЗИ и ЭП'
        verbose_name_plural = 'СЗИ и ЭП'

    def __str__(self):
        return f'{self.name}'


class NpaLinks(TranslatableModel):
    translations = TranslatedFields(
        description=models.TextField(blank=False, null=False, verbose_name='Описание'),
    )
    link = models.URLField(max_length=255, blank=False, null=True, verbose_name='Ссылка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Ссылка на НПА'
        verbose_name_plural = 'Ссылки на НПА'

    def __str__(self):
        return f'{self.description}'

