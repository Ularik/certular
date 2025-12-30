from django.contrib import admin
from .models import Messages
from .filters import DateFilter, UserFilter



@admin.register(Messages)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_filter = [UserFilter, DateFilter]
    fieldsets = (
        (None, {'fields': ('id', 'name', 'description', 'user', 'phone_number', 'email', 'file', 'created_at')}),
    )
    readonly_fields = ['id', 'user', 'created_at', 'email']



