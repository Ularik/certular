from ninja import Router, UploadedFile, File
from .schema import ReportCreateSchema
from django.contrib.auth import get_user_model
from accounts_app.models import Organization
from .models import Reports

User = get_user_model()
router = Router()

@router.post('/report-create', response={201: str, 400: str})
def create_report(request, body: ReportCreateSchema, file: File[UploadedFile]):
    report_body = body.dict(exclude_unset=True)
    user = User.objects.filter(first_name=report_body['username']).first()
    organization = Organization.objects.filter(name=report_body['organization']).first()

    if not (user and organization):
        return 400, 'Нет такого пользователя или организации'

    report = Reports(user=user, organization=organization, name=report_body['attack_type'])
    report.file.save(file.name, file)
    report.save()
    return 201, 'Успешно создан'