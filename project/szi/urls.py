from django.urls import path
from .views import crypto_szi_view, crypto_signature_view, get_encrypted_tools

app_name = 'crypto'

urlpatterns = [
    path('szi/', crypto_szi_view, name='szi'),
    path('signature/', crypto_signature_view, name='signature'),
    path('encrypted_tools/', get_encrypted_tools, name='encrypted_tools'),
]
