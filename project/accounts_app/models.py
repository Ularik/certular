import random
import string
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, UserManager
from project import settings
from django.contrib.auth.models import Group
from django.core.validators import MaxLengthValidator, RegexValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

TELEPHONE = RegexValidator(r'^\d+$', 'Only numeric characters are allowed.')


class Groups(Group):
    class Meta:
        app_label = 'accounts_app'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Organization(models.Model):
    name = models.TextField(blank=False, null=False, verbose_name='Наименование')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'Organization'
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


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
        user.save(using=self._db)
        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', blank=True, null=True)
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    position = models.CharField(max_length=200, blank=True, null=True, verbose_name='Должность')
    organization = models.ForeignKey(to=Organization, blank=True, null=True, verbose_name='Организация',
                                     related_name='user', on_delete=models.SET_NULL)
    email = models.EmailField(verbose_name='Email', unique=True)
    number = models.CharField(max_length=19, blank=False, null=False, verbose_name='Мобильный номер',
                              validators=[TELEPHONE, MaxLengthValidator])
    is_admin = models.BooleanField(default=False)

    class Meta:
        app_label = 'accounts_app'
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'date_of_birth']

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

