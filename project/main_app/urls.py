from django.urls import path
from django.urls import path, include
from .views import MainIndex, SearchIndex, chart_view

app_name = 'main_app'

urlpatterns = [
    path('', MainIndex.as_view(), name='index'),
    path('search/', SearchIndex.as_view(), name='search_index'),
    path('chart/', chart_view, name='chart'),
]
