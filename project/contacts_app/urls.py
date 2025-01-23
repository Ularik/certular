from django.urls import path
from .views import ContactsDetailView

app_name = 'contacts'

urlpatterns = [
    # path('', AboutListView.as_view(), name='about'),
    path('', ContactsDetailView.as_view(), name='contact_detail')
]