from django.contrib import admin

from .models import Reports


class ReportsAdmin(admin.ModelAdmin):
    search_fields = ('name', 'created_date', 'user__username', 'status')
    list_display = ['created_date', 'user', 'organization', 'name', 'status']
    ordering = ['-created_date']
    list_filter = ['organization']
    fields = ['organization', 'name', 'file', 'user', 'status', 'watched_date', 'read_date']
    readonly_fields = ['id', 'user', 'status', 'watched_date', 'read_date']

    def save_model(self, request, obj, form, change):
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
        super().save_model(request, obj, form, change)

admin.site.register(Reports, ReportsAdmin)
