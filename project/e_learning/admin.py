from django.contrib import admin
from .models import ELearning
from parler.admin import TranslatableAdmin


@admin.register(ELearning)
class AboutAdmin(TranslatableAdmin):
    list_display = ['name', 'language_column']
    fieldsets = (
        (None, {
            'fields': ('name', 'link')
        }),
    )