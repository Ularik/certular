from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from reports_app.models import Reports
from .models import Organization, User, Groups


class UserInline(admin.TabularInline):
    model = User
    fields = ('first_name', 'last_name', 'patronymic',)
    extra = 0  # Количество пустых строк для добавления новых объектов
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    inlines = [UserInline]
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    fields = ('name',)


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name',)
    list_filter = ('first_name', 'last_name')
    # raw_id_fields = ['organization']  # test

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Организация', {'fields': ('organization',)}),
        ('Персональные данные', {'fields': ('first_name', 'last_name', 'patronymic',
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
                       'organization', 'number'),
        }),
    )
    search_fields = ('email', )
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Groups)
