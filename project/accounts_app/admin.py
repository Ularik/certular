from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import Groups
from .models import Organization, User


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    fields = ('name',)


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name',)
    list_filter = ('first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Организация', {'fields': ('organization',)}),
        ('Персональные данные', {'fields': ('first_name', 'last_name', 'patronymic', 'date_of_birth',
                                            'position')}),
        ('Привилегии', {'fields': ('groups',)}),
        ('Активность пользователя', {'fields': ('is_active',)}),
        ('Номер телефона', {'fields': ('number',)}),
        ('Безопасность', {'fields': ('password',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2', 'is_superuser',
                       'organization', 'date_of_birth', 'number'),
        }),
    )
    search_fields = ('email', )
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Groups)
