from django.contrib import admin
from .models import CryptoProvider, NpaLinks, Applicant, EncryptionTools
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


@admin.register(Applicant)
class ApplicantAdmin(TranslatableAdmin):
    list_display = ['index', 'address', 'phone']
    fieldsets = (
        (None, {'fields': ('index', 'address', 'phone')}),
    )


@admin.register(EncryptionTools)
class EncryptionToolsAdmin(TranslatableAdmin):
    list_display = ['number', 'title']
    search_fields = ('translations__number', 'translations__title', 'translations__applicant__index')
    fieldsets = (
        (None, {
            'fields': ('number', 'add_date', 'validity_period', 'title', 'npa_links', 'components',
                       'testing_lab', 'applicant', 'finish_info'),
        }),
    )


@admin.register(NpaLinks)
class NpaLinksAdmin(TranslatableAdmin):
    list_display = ['description', 'link', 'created_at']
    search_fields = ('translations__description', 'translations__link')
    fieldsets = (
        (None, {'fields': ('description', 'link', 'created_at')}),
    )
    readonly_fields = ['created_at']


