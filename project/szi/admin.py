from django.contrib import admin
from .models import CryptoProvider, NpaLinks
from parler.admin import TranslatableAdmin


@admin.register(CryptoProvider)
class CryptoProviderAdmin(TranslatableAdmin):
    list_display = ['title', 'name', 'language_column']
    fieldsets = (
        (None, {
            'fields': ('title', 'name', 'description', 'crypto_npa', 'npa_links', 'created_at'),
        }),
    )
    readonly_fields = ('created_at',)


@admin.register(NpaLinks)
class AboutAdmin(TranslatableAdmin):
    list_display = ['link', 'description']
    fieldsets = (
        (None, {
            'fields': ('description', 'link', 'created_at')
        }),
    )
    readonly_fields = ['created_at']

