from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import News, NewsGalleryItem
from django.utils.safestring import mark_safe
from parler.admin import TranslatableAdmin


class NewsGalleryItemAdminInline(TabularInline):
    extra = 1
    model = NewsGalleryItem
    fields = ('file_news', )


@admin.register(News)
class NewsAdmin(TranslatableAdmin):
    list_display = ['name', 'language_column']
    inlines = (NewsGalleryItemAdminInline,)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'full_description', 'cover', 'get_image', 'created_at'),
        }),
    )
    readonly_fields = ('get_image', 'created_at')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.cover.url} width=200 height=150>')

    get_image.short_description = 'Изображение Обложки'
