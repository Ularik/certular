from django import forms
# from apps.snowpenguin.django.recaptcha3.fields import ReCaptchaField
from .models import Appeal


class AddAppealForm(forms.ModelForm):
    # captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = 'Выберите из выподающего списка'

    class Meta:
        model = Appeal
        fields = ['full_name', 'email', 'message', 'organization', 'phone_number']    # captcha

