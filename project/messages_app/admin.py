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
    list_display = ['id', 'user__first_name', 'created_at']
    list_filter = [UserFilter, DateFilter]
    fieldsets = (
        (None, {'fields': ('id', 'description', 'user', 'file', 'created_at')}),
    )
    readonly_fields = ['id', 'created_at', 'get_full_name', 'get_number', 'get_email']

    def get_org_name(self, obj):
        if hasattr(obj, 'organization'):
            return f'{obj.user.organization.name}'
        else:
            return f'Без организации'

    get_org_name.short_description = 'Организация'

    def get_full_name(self, obj):
        if obj.user:
            l_name = obj.user.last_name
            patr = obj.user.patronymic
            if not obj.user.last_name:
                l_name = ''
            if not obj.user.patronymic:
                patr = ''
            return f'{obj.user.first_name} {l_name} {patr}'
        else:
            return f'{obj.full_name}'

    get_full_name.short_description = 'ФИО пользователя'

    def get_number(self, obj):
        if obj.user:
            return f'+{obj.user.number}'
        else:
            return f'+{obj.phone_number}'

    get_number.short_description = 'Мобильный номер пользователя'

    def get_email(self, obj):
        if obj.user:
            return f'{obj.user.email}'
        else:
            return f'{obj.email}'

    get_email.short_description = 'Почта пользователя'


