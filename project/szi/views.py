from django.shortcuts import render
import logging
from .models import CryptoProvider, EncryptionTools


logger = logging.getLogger(__name__)


def crypto_signature_view(request):
    crypto_signature = CryptoProvider.objects.filter(title='signature').first()
    text = crypto_signature.description.split('\n')
    act_links = crypto_signature.npa_links.all()
    act_files = crypto_signature.crypto_npa.all()

    context = {}
    context['title'] = crypto_signature.name
    context['paragraph_first'] = text[1]
    context['paragraph_second'] = text[2]
    context['paragraph_third'] = text[3]
    context['paragraph_fourth'] = text[4]
    context['paragraph_fifth'] = text[5]
    context['paragraph_sixth'] = text[6]
    context['acts_start'] = text[0]
    context['acts_links'] = act_links
    context['act_files'] = act_files

    return render(request, 'crypto_provider/signature.html', context)


def get_encrypted_tools(request):
    tools_list = list(EncryptionTools.objects.all())  # Сначала создаем список
    tools_list.sort(key=lambda word: int(word.number[-5:]))
    return render(request, 'crypto_provider/encryptions_table.html', {'tools': tools_list})