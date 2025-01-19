from django.contrib import admin
from .models import About, CenterTasks
from parler.admin import TranslatableAdmin


@admin.register(About)
class AboutAdmin(TranslatableAdmin):
    list_display = ['language_column']
    fieldsets = (
        (None, {
            'fields': ('description', )
        }),
    )
    # readonly_fields = ['created_at']


@admin.register(CenterTasks)
class AboutAdmin(TranslatableAdmin):
    list_display = ['description', 'language_column']
    fieldsets = (
        (None, {
            'fields': ('description', )
        }),
    )
    readonly_fields = ['created_at']
