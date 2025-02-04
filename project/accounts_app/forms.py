from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class MyRegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'email',

            'position',
            'organization',
            'number',
        )
