from django.shortcuts import render
from django.views.generic import ListView
from .models import Reports
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, JsonResponse
from django.utils import timezone
from .serializers import ReportsListSerializer
import zipfile
import json
from django.conf import settings
import os
import io


logger = logging.getLogger(__name__)


class ReportsListView(LoginRequiredMixin, ListView):
    queryset = Reports.objects.all()
    template_name = 'reports/reports.html'
    context_object_name = 'reports'
    login_url = '/ru/'

    def get_queryset(self):
        queryset = Reports.objects.filter(organization=self.request.user.organization)
        return queryset


def get_reports_list(request):
    queryset = Reports.objects.filter(organization=request.user.organization)

    reports_not_watched = queryset.filter(watched_date__isnull=True)  # 1 - статус: Не просмотрен (Только отправлен)
    if reports_not_watched:
        reports_not_watched.update(status=2)
        reports_not_watched.update(watched_date=datetime.now())
        logger.info(f'{request.user} просмотрел страницу отчетов сейчас в - '
                    f'{datetime.now().strftime('%d:%m:%Y - %H:%M')}')

    serializer = ReportsListSerializer(queryset, many=True)
    response = JsonResponse(serializer.data, safe=False, status=200)
    response['Cache-Control'] = 'no-store'
    return response


@csrf_exempt
def download_report(request, report_id):
    report = Reports.objects.filter(id=report_id).first()

    if not report.read_date:
        report.status = 3  # Прочитан
        report.read_date = datetime.now()
        report.save()
        logger.info(f'{request.user} скачал отчёт №{report_id} сейчас в - '
                    f'{datetime.now().strftime('%d:%m:%Y - %H:%M')}')

    # Возвращаем файл пользователю
    response = FileResponse(open(report.file.path, 'rb'), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{report.file.name}"'
    return response


@csrf_exempt
def dowload_zip_reports(request):
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, 'w') as zipf:
        reports_id = json.loads(request.body)
        for report_id in reports_id:
            report = Reports.objects.filter(id=report_id).first()
            if report.file:
                file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/' + report.file.url
                filename = os.path.basename(file_path)
                zipf.write(file_path, arcname=filename)

    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='archive.zip', content_type='application/zip')



def change_report_status(request, report_id):

    report = Reports.objects.filter(id=report_id).first()
    report.read_date = timezone.now()

    if report.status == 4:
        report.status = 3
        report.save()
        return JsonResponse({'status': 3}, status=200)

    report.status = 4
    report.save()
    print(f'Статус изменен на: {report.status}')

    return JsonResponse({'status': 4}, status=200)



def forbidden_auth(request):
    return render(request, 'forbidden/not_authenticated_error.html')
