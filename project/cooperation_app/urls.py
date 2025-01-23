from django.urls import path
from .views import CooperationsListView

app_name = 'cooperation_app'

urlpatterns = [
    path('', CooperationsListView.as_view(), name='cooperations')
]
