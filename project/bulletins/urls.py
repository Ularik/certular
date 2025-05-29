from django.urls import path
from .views import BulletinsListView, get_bulletins

app_name = 'bulletins'

urlpatterns = [
    path('', BulletinsListView.as_view(), name='bulletins_list'),
    path('get_list/', get_bulletins)
]