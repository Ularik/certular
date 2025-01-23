from django.contrib import admin
from .models import Cooperation
from parler.admin import TranslatableAdmin


@admin.register(Cooperation)
class AboutAdmin(TranslatableAdmin):
    list_display = ['name', 'language_column']
    fieldsets = (
        (None, {
            'fields': ('name', 'link', 'image')
        }),
    )