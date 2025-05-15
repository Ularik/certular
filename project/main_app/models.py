from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class ChartLink(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # Например, для формирования URL

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Метод для получения URL проекта
        from django.urls import reverse
        return reverse('main_app:chart')

    class Meta:
        verbose_name = 'Граффик'
        verbose_name_plural = 'Граффики'


class SeoPages(TranslatableModel):
    translations = TranslatedFields(
        meta_tag_title=models.CharField(max_length=255, verbose_name='Заголовок страницы'),
        meta_tag_keywords=models.TextField(verbose_name='Ключевые слова'),
        meta_tag_description=models.TextField(verbose_name='Описание страницы')
    )

    page_name = models.CharField(max_length=255, verbose_name='Название страницы')

    class Meta:
        db_table = 'seo_pages'
        verbose_name = 'Сео страница'
        verbose_name_plural = 'Сео страница'

