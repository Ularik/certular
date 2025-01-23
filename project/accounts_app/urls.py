from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import RegistrationAPIView, login_view, logout_view

app_name = 'accounts_app'

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]