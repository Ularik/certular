from django.urls import path
from .views import appeals_post


urlpatterns = [
    path('', appeals_post, name='appeals'),
]