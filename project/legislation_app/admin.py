from django.contrib import admin
from .models import Legislation, Regulations
from parler.admin import TranslatableAdmin


@admin.register(Legislation)
class LegislationAdmin(TranslatableAdmin):
    list_display = ['name', 'language_column']
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'created_at')
        }),
    )
    readonly_fields = ['created_at']


@admin.register(Regulations)
class RegulationsAdmin(TranslatableAdmin):
    list_display = ['description', 'link']
    search_fields = ('translations__description',)
    fieldsets = (
        (None, {
            'fields': ('description', 'link', 'created_at')
        }),
    )
    readonly_fields = ['created_at']
