from django.contrib import admin
from .models import Contacts
from parler.admin import TranslatableAdmin


@admin.register(Contacts)
class ContactsAdmin(TranslatableAdmin):
    list_display = ('email', 'language_column')
    fieldsets = (
        (None, {
            'fields': ('address', 'phone', 'email'),
        }),
    )
