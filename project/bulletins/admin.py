from django.contrib import admin
from .models import Bulletins
from parler.admin import TranslatableAdmin


@admin.register(Bulletins)
class NotificationAdmin(TranslatableAdmin):
    list_display = ['title', 'language_column']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'created_at'),
        }),
    )
    readonly_fields = ('created_at',)
