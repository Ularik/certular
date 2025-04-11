from django import template
from django.conf import settings

from accounts_app.forms import MyRegisterUserForm
from e_learning.models import ELearning
from contacts_app.models import Contacts
from cyber_security_app.models import *
from about_app.models import About
from accounts_app.models import Organization

register = template.Library()


@register.simple_tag()
def get_cyber_security():
    return CyberSecurity.objects.all()


@register.simple_tag()
def get_about():
    return About.objects.all().first()


@register.simple_tag()
def get_about_desktop():
    context = {
        'about': About.objects.all().first()
    }
    return context


@register.simple_tag()
def get_e_learning_desktop():
    e_learning = ELearning.objects.all().first()
    if e_learning:
        link = e_learning.link
    else:
        link = '#'
    return {'link': link}

@register.simple_tag()
def get_cyber_threat_database():
    link = 'http://base.cert.gov.kg/'
    return {'link': link}


@register.simple_tag()
def get_contacts():
    return Contacts.objects.first()


@register.simple_tag()
def get_organizations():
    return Organization.objects.all()


@register.simple_tag()
def get_site_recaptcha():
    return settings.RECAPTCHA_PUBLIC_KEY

@register.simple_tag()
def register_form():
    form = MyRegisterUserForm()
    return form


# @register.simple_tag()
# def messages_form():
#     form = CheckRecaptcha()
#     return form
