from django.urls import path, include
from .views import LegislationView

app_name = 'legislation_app'

urlpatterns = [
    path('', LegislationView.as_view(), name='legislation'),
]
