from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from apps.accounts_apps.views import registration_post, RegistrationAPIView, check_registration, EmailBackend, \
    login_user, login_keyclock, auth

app_name = 'account_apps'

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', login_user, name='login'),
    path('login/keyclock/', login_keyclock, name='login_keyclock'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check/registration/', check_registration, name='check_registration'),
]