from django.urls import path
from .views import ReportsListView, download_report, change_report_status

app_name = 'reports_app'

urlpatterns = [
    path('', ReportsListView.as_view(), name='reports'),
    path('download/<int:report_id>/', download_report, name='download_report'),
    path('change/<int:report_id>/', change_report_status, name='change_status')
]