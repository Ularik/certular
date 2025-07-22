from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group
from django.core.validators import MaxLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import requests

TELEPHONE = RegexValidator(r'\^+\d+$', 'Only numeric characters are allowed.')


class Groups(Group):
    class Meta:
        app_label = 'accounts_app'
        verbose_name = _('Группа')
        verbose_name_plural = _('Группы')


class Organization(models.Model):
    name = models.CharField(verbose_name=_('Наименование'), unique=True)

    def __str__(self):
        admin = _("Админ")
        return f'{self.name or admin}'

    class Meta:
        db_table = 'Organization'
        verbose_name = _('Организация')
        verbose_name_plural = _('Организации')

    def save(self, *args, **kwargs):
        if not self.pk:  # Проверяем только при создании
            if Organization.objects.filter(name__iexact=self.name).exists():
                raise ValidationError(_("Организация с таким именем уже существует"))
        super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a name")

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None, **extra_fields):
        user = self.create_user(email, first_name, password, **extra_fields)
        user.is_admin = True

        # 👇 Отправляем запрос на второй сервис
        try:
            self._create_remote_user(first_name, password)
        except Exception as e:
            # Логировать ошибку или выбросить, по необходимости
            print(f'Не удалось создать суперпользователя во втором сервисе: {e}')

        user.save(using=self._db)
        return user

    def _create_remote_user(self, username, password):
        url = 'http://127.0.0.1:8000/api/events/user-create'
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "username": username,
            "password": password,
            "is_staff": True
        }

        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()  # выбросит ошибку если код ответа != 2xx


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=False, blank=True, null=True)
    first_name = models.CharField(max_length=100, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=100, verbose_name=_('Фамилия'), blank=True, null=True)
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Отчество'))
    position = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Должность'))
    organization = models.ForeignKey(to=Organization, blank=True, null=True, verbose_name=_('Организация'),
                                     related_name='user', on_delete=models.SET_NULL)
    email = models.EmailField(verbose_name='Email', unique=True)
    number = models.CharField(max_length=19, blank=False, null=False, verbose_name=_('Мобильный номер'))
    is_admin = models.BooleanField(default=False)

    class Meta:
        app_label = 'accounts_app'
        verbose_name = _('Пользователи')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return f'{self.first_name or self.username}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        """Does the myuser have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the myuser have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the myuser a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin



