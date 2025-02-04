from django.urls import path
from .views import NewsListView, NewsDetailView, notification_view

app_name = 'news'

urlpatterns = [
    path('', NewsListView.as_view(), name='news'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('notification/', notification_view, name='notification_detail')
]
