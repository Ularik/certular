from django.urls import path
from .views import ReportsListView, download_report, change_report_status, get_reports_list, dowload_zip_reports

app_name = 'reports_app'

urlpatterns = [
    path('', ReportsListView.as_view(), name='reports'),
    path('reports_list/', get_reports_list, name='reports_list'),
    path('download/<int:report_id>/', download_report, name='download_report'),
    path('change/<int:report_id>/', change_report_status, name='change_status'),
    path('download-zip/', dowload_zip_reports, name='download_zip')
]