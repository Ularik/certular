from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, forms


class MyRegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'email',
            'date_of_birth',
            'position',
            'organization',
            'number',
        )