from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import CyberSecurity, CyberIncident


@admin.register(CyberSecurity)
class AboutAdmin(TranslatableAdmin):
    list_display = ['name', 'language_column']
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'image',
                'created_at',
            )
        }),
    )
    readonly_fields = ['created_at']


@admin.register(CyberIncident)
class IncidentAdmin(TranslatableAdmin):
    list_display = ['language_column']
    fieldsets = (
        (None, {
            'fields': (
                'description',
                'created_at',
            )
        }),
    )
    readonly_fields = ['created_at']