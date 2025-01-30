from django.contrib.auth import get_user_model
from django.db import models

from accounts_app.models import Organization


User = get_user_model()

class Reports(models.Model):
    user = models.ForeignKey(to=User, null=True, blank=True, verbose_name='Пользователь', on_delete=models.CASCADE)
    organization = models.ForeignKey(to=Organization, null=False, blank=False,
                                     verbose_name='Организация', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Название', null=False, blank=False)
    file = models.FileField(upload_to='reports_files', verbose_name='Файл', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    watched_date = models.DateTimeField(null=True, blank=True)
    read_date = models.DateTimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=(
        (1, 'Отправлен'),
        (2, 'Просмотрена страница'),
        (3, 'Прочитан документ'),
        (4, 'Выполнен')
    ), default=1)

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'

    def __str__(self):
        return self.name



