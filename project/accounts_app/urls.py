from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import RegistrationAPIView, login_view, logout_view, check_registration, answer_after_reg

app_name = 'accounts_app'

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('check/registration/', check_registration, name='check'),
    path('answer/registration/', answer_after_reg, name='answer_reg'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]