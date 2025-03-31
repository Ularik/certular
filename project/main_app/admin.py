from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import SeoPages

from django.utils.html import format_html
from .models import ChartLink

@admin.register(ChartLink)
class ChartLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_to_project')  # Добавляем поле в список отображаемых колонок

    def link_to_project(self, obj):
        # Метод для отображения ссылки
        url = obj.get_absolute_url()
        return format_html('<a href="{}" target="_blank">Перейти к граффикам</a>', url)

    link_to_project.short_description = 'Ссылка на проект'  # Название колонки в


@admin.register(SeoPages)
class SeoPageAdmin(TranslatableAdmin):
    list_display = ['page_name', 'language_column']
    fieldsets = (
        (None, {
            'fields': ('page_name', 'meta_tag_title', 'meta_tag_keywords', 'meta_tag_description'),
        }),
    )
