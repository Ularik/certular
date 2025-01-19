from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import CyberSecurity


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
