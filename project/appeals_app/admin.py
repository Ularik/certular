from django.contrib import admin
from .models import Appeal


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'organization', 'created_at', 'email', 'phone_number']
    fields = ['full_name', 'email', 'phone_number', 'message']
    search_fields = ['full_name', 'email', 'phone_number', 'message']
    readonly_fields = ['id']

