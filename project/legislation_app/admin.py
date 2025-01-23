from django.contrib import admin
from .models import Legislation, Regulations
from parler.admin import TranslatableAdmin


@admin.register(Legislation)
class AboutAdmin(TranslatableAdmin):
    list_display = ['name', 'language_column']
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'created_at')
        }),
    )
    readonly_fields = ['created_at']


@admin.register(Regulations)
class AboutAdmin(TranslatableAdmin):
    list_display = ['link', 'language_column']
    fieldsets = (
        (None, {
            'fields': ('description', 'link', 'created_at')
        }),
    )
    readonly_fields = ['created_at']
    # language_column.short_description = 'Языки'
