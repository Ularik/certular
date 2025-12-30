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
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
    )
    npa_links = models.ManyToManyField('NpaLinks', null=True, blank=True)
    crypto_npa = models.ManyToManyField(NotificationNpa, null=True, blank=True)

    class Meta:
        db_table = 'CryptoProvider'
        verbose_name = 'СЗИ и ЭП'
        verbose_name_plural = 'СЗИ и ЭП'

    def __str__(self):
        return f'{self.name}'


class NpaLinks(TranslatableModel):
    translations = TranslatedFields(
        description=models.TextField(blank=False, null=False, verbose_name='Описание'),
        link = models.URLField(max_length=255, blank=False, null=True, verbose_name='Ссылка'),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Ссылка на НПА'
        verbose_name_plural = 'Ссылки на НПА'

    def __str__(self):
        return f'{self.description}'


class Applicant(TranslatableModel):
    translations = TranslatedFields(
        index=models.CharField(max_length=120, verbose_name='Индекс'),
        address = models.CharField(max_length=155, verbose_name='Адресс')
    )
    phone = models.CharField(max_length=19, blank=True, null=True, verbose_name='Мобильный номер')

    class Meta:
        verbose_name = 'Заявитель'
        verbose_name_plural = 'Заявители'

    def __str__(self):
        return f'{self.index}'


class EncryptionTools(TranslatableModel):
    npa_links = models.ManyToManyField(NpaLinks,
                                       verbose_name='Наименования документов, требованиям которых соответсвует СЗИ')
    applicant = models.ForeignKey(Applicant, on_delete=models.SET_NULL, null=True, blank=True)
    translations = TranslatedFields(
        number=models.CharField(max_length=125, verbose_name='Номер сертификата'),
        title=models.CharField(max_length=125, verbose_name='Наименование средства(шифр)'),
        components=models.CharField(max_length=100, verbose_name='Схема сертификации, кол-во СЗИ'),
        testing_lab=models.CharField(max_length=125, verbose_name='Испытательная лаборатория'),
        finish_info=models.TextField(verbose_name='Информация об окончании срока тех поддержки', null=True, blank=True),
        add_date=models.CharField(max_length=80, verbose_name='Дата добавления средства'),
        validity_period=models.CharField(max_length=80, verbose_name='Срок действия'),
    )
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Средства сертификации'
        verbose_name_plural = 'Средства сертификации'

    def __str__(self):
        return f'{self.pk}'