import datetime

from django.urls import reverse
from tinymce.models import HTMLField
from PIL import Image, ExifTags
from io import BytesIO
from django.conf import settings
from django.core.files import File
from pathlib import Path
from django.db import models
from factory.django import mute_signals
from parler.models import TranslatableModel, TranslatedFields
from apps.utils import content_file_name
from mimetypes import guess_type
from django_resized import ResizedImageField
import os
from subprocess import call
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete

from core.settings import BASE_DIR
from core.tasks import convert_webm_mp4_module


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


@mute_signals(post_save)
def convert_video(instance):
    path_start = settings.MEDIA_ROOT + '/News_gallery/' + str(datetime.datetime.today().date()) + '/'
    format_name = Path(instance.file_news.file.name).name.split(".")[-1]
    # print('format', Path(instance.file_news.file.name).name.split(".")[-1])
    input_file = path_start + Path(instance.file_news.file.name).name
    output_file = path_start + Path(instance.file_news.file.name).name.replace(f'.{format_name}', '.webm')
    # print(input_file)
    # print(output_file)
    # print(Path(instance.file_news.file.name).name.replace(f'.{format_name}', '.webm').split('/')[0])
    # print('self_file_name', instance.file_news.name)
    # print('self_file_name 2', instance.file_news.name)
    path_name = instance.file_news.name
    change_path = Path(instance.file_news.file.name).name.split("/")[0]
    # print(change_path)
    to_path = Path(instance.file_news.file.name).name.replace(f'.{format_name}', '.webm').split('/')[0]
    # print('path_name', path_name)
    # print('to_path', to_path)
    replace_path_name = instance.file_news.name.replace(f'{change_path}', f'{to_path}')
    print('replace_path_name', replace_path_name)
    # print(instance.file_news.path)
    # os.remove(instance.file_news.path)
    instance.file_news.name = replace_path_name
    # print(instance.file_news)
    convert_webm_mp4_module.delay(input_file, output_file, instance.file_news.path)
    instance.save()


@mute_signals(post_save)
def convert_image(instance):
    # print('zdesss')
    # print('da image')
    # print('smena formata image')
    img = Image.open(BytesIO(instance.file_news.read()))
    img_filename = Path(instance.file_news.file.name).name.split(".")[0]
    # img_filename = Path(self.file_news.file.name).name
    # print('img_file name', img_filename)
    # Spilt the filename on “.” to get the file extension only
    # img_suffix = Path(self.file_news.file.name).name.split(".")[-1]
    # print('img_suffix suffix', img_suffix)
    # print(img)

    img.thumbnail((1080, 1080), Image.ANTIALIAS)
    output = BytesIO()
    img.save(output, format='WEBP', quality=90)
    output.seek(0)
    # print(instance.file_news.path)
    os.remove(instance.file_news.path)
    instance.file_news = File(output, img_filename + '.webp')
    # print(instance.file_news)
    instance.save()


@receiver(post_save, sender=NewsGalleryItem)
def convert_file(sender, **kwargs):
    instance = kwargs.get('instance')
    type_tuple = ''
    if instance.file_news:

        type_tuple = guess_type(instance.file_news.url, strict=True)

        print(type_tuple)
        try:
            if (type_tuple[0]).__contains__("image"):
                convert_image(instance)
            else:
                # if instance.file_news.file.name.endswith('.webm'):
                #     pass
                convert_video(instance)
        except:
            return


@receiver(pre_delete, sender=NewsGalleryItem)
def on_delete(sender, **kwargs):
    # print(sender)
    print('zdessss')
    instance = kwargs.get('instance')
    if instance._state.adding and not instance.pk:
        return False
    # try:
    #     old_file = sender.objects.get(pk=instance.pk).file_news
    #     print(old_file, 'olllllllddddddddfillleeeeee')
    # except sender.DoesNotExist:
    #     return False
    # old_file = sender.objects.get(pk=instance.pk).file_news
    # print(old_file, 'old file')
    file = instance.file_news
    print('file', file)
    if file:
        # if not old_file == file:
        if os.path.isfile(file.path):
            os.remove(file.path)
