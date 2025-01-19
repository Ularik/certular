from django import forms
from .models import User


class MyRegisterUserForm(forms.ModelForm):

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