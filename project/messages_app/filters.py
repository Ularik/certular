from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext


class InputFilter(admin.SimpleListFilter):
    template = 'admin/filter.html'

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class UserFilter(InputFilter):
    parameter_name = 'user'
    title = gettext('Пользователь')

    def queryset(self, request, queryset):
        if self.value() is not None:
            name = self.value()
            return queryset.filter(user__first_name__icontains=name)


class DateFilter(InputFilter):
    parameter_name = 'date'
    title = gettext('Дата')

    def queryset(self, request, queryset):
        if self.value() is not None:
            date = self.value()
            return queryset.filter(created_at__icontains=date)




