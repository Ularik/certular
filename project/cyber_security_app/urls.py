from django.urls import path
from .views import CyberSecurityView, CyberSecurityListView

app_name = 'cyber_security'

urlpatterns = [
    path('<int:pk>/', CyberSecurityView.as_view(), name='cyber_security'),
    path('list/', CyberSecurityListView.as_view(), name='cyber_security_list')
]