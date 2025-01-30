from django.urls import path
from .views import appeals_post


app_name = 'appeals_app'

urlpatterns = [
    path('', appeals_post, name='appeals'),
]