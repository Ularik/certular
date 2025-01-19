from django.urls import path
from .views import AboutTypeView, AboutDetailView

app_name = 'about'

urlpatterns = [
    path('list/', AboutTypeView.as_view(), name='about'),
    path('', AboutDetailView.as_view(), name='about_detail')
]