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

    if body.username:
        user = User.objects.filter(first_name=body.username).first()
        report_body['user'] = user

    organization = Organization.objects.filter(org_code__icontains=report_body['organization']).first()
    report_body['organization'] = organization

    if not organization:
        return 400, 'Нет такогой организации'

    report = Reports(**report_body)
    report.file.save(file.name, file)
    report.save()
    return 201, 'Успешно создан'