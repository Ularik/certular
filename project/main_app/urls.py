from django.urls import path
from django.urls import path, include
from .views import MainIndex, SearchIndex, chart_view, RobotTxtView, chart_data

app_name = 'main_app'

urlpatterns = [
    path('', MainIndex.as_view(), name='index'),
    path('search/', SearchIndex.as_view(), name='search_index'),
    path('chart/', chart_view, name='chart'),
    path('chart_data/', chart_data, name='chart_data'),
    path('cti/', RobotTxtView.as_view()),
]
