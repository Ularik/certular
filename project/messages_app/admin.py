import uuid
from django.contrib import admin
from .models import Messages
from django.http import HttpResponseRedirect
from .filters import DateFilter, UserFilter
from thehive4py.api import TheHiveApi
from thehive4py.auth import BearerAuth
from thehive4py.exceptions import AlertException
from thehive4py.models import Version, Alert, AlertArtifact, CustomFieldHelper, Case
from django.conf import settings


@admin.register(Messages)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_filter = [UserFilter, DateFilter]
    fieldsets = (
        (None, {'fields': ('id', 'name', 'description', 'user', 'phone_number', 'email', 'file', 'created_at')}),
    )
    readonly_fields = ['id', 'user', 'created_at', 'email']



