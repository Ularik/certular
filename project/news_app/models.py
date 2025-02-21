import datetime
from django.urls import reverse
from tinymce.models import HTMLField
from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from mimetypes import guess_type
from django_resized import ResizedImageField


def content_file_name(directory):
    # file will be uploaded to MEDIA_ROOT/customers/yearmonthday/<filename>
    today = datetime.date.today().strftime("%Y-%m-%d")
    return "{directory}/{date}".format(directory=directory, date=today)


class News(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, blank=False, null=False, verbose_name='Наименование'),
        description=models.TextField(blank=False, null=False, verbose_name='Краткое описание'),
        full_description=HTMLField(verbose_name='Подробное описание')
    )
    cover = ResizedImageField(crop=['middle', 'center'], quality=80,
                              upload_to=content_file_name('News'), blank=False, force_format='WEBP',
                              null=True, verbose_name='Обложка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        db_table = 'News'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'pk': self.pk})


class NewsGalleryItem(models.Model):

    file_news = models.FileField(upload_to=content_file_name('News_gallery'), null=True, blank=True,
                                 verbose_name='Файлы новостей')
    news = models.ForeignKey(to=News, on_delete=models.CASCADE, related_name='gallery_news')

    class Meta:
        db_table = 'newsgalleryitems'

    def media_type_html(self):
        """
        guess_type returns a tuple like (type, encoding) and we want to access
        the type of media file in first index of tuple
        """
        type_tuple = guess_type(self.file_news.url, strict=True)
        if (type_tuple[0]).__contains__("image"):
            return "image"
        elif (type_tuple[0]).__contains__("video"):
            return "video"


class Notification(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200, blank=False, null=False, verbose_name='Наименование'),
        description=models.TextField(blank=False, null=False, verbose_name='Описание'),
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    )
    notification_npa = models.ManyToManyField('NotificationNpa')
    class Meta:
        db_table = 'Notification'
        verbose_name = 'Нотификация'
        verbose_name_plural = 'Нотификация'

    def __str__(self):
        return f'{self.name}'


class NotificationNpa(TranslatableModel):
    translations = TranslatedFields(
        name=models.TextField(verbose_name='Наименование'),
        file = models.FileField(upload_to=content_file_name('laws'), null=True, blank=True)
    )

    class Meta:
        verbose_name = 'Файлы актов'
        verbose_name_plural = 'Файлы актов'

    def __str__(self):
        return self.name