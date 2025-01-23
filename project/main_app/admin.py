from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import SeoPages


# Register your models here.
@admin.register(SeoPages)
class SeoPageAdmin(TranslatableAdmin):
    list_display = ['page_name', 'language_column']
    fieldsets = (
        (None, {
            'fields': ('page_name', 'meta_tag_title', 'meta_tag_keywords', 'meta_tag_description'),
        }),
    )
