from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
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
    list_display = ('org_code', 'id', 'name',)
    list_filter = ('org_code', 'id', 'name',)
    search_fields = ('org_code', 'name',)
    fields = ('org_code', 'name',)


PHONE_PLACEHOLDER = '+996 (555) 12-34-56'
PHONE_VALIDATOR = RegexValidator(
    r'^\+?[\d\s()\-]{9,19}$',
    f'Введите номер телефона в формате {PHONE_PLACEHOLDER}',
)


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name',)
    list_filter = ('first_name', 'last_name')
    # raw_id_fields = ['organization']  # test

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Организация', {'fields': ('organization',)}),
        ('Персональные данные', {'fields': ('first_name', 'last_name', 'patronymic',
                                            'position')}),
        ('Привилегии', {'fields': ('is_admin', 'groups',)}),
        ('Активность пользователя', {'fields': ('is_active',)}),
        ('Номер телефона', {'fields': ('number',)}),
        ('Безопасность', {'fields': ('password',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2', 'is_admin',
                       'organization', 'number'),
        }),
    )
    search_fields = ('email', )
    ordering = ('email',)
    filter_horizontal = ()

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'number':
            formfield.widget.attrs['placeholder'] = PHONE_PLACEHOLDER
            formfield.help_text = f'Образец: {PHONE_PLACEHOLDER}'
            formfield.validators.append(PHONE_VALIDATOR)
        return formfield


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Groups)
