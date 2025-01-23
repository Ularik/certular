from django.db import models
from parler.models import TranslatableModel, TranslatedFields


# Create your models here.

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
