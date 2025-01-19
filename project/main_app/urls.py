from django.urls import path
from django.urls import path, include
from .views import MainIndex, SearchIndex

app_name = 'main_apps'

urlpatterns = [
    path('', MainIndex.as_view(), name='index'),
    path('search/', SearchIndex.as_view(), name='search_index'),
]
