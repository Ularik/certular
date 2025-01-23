from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Legislation, Regulations
from main_app.models import SeoPages


class LegislationView(TemplateView):
    template_name = 'legislation/legislation.html'

    def get_context_data(self, **kwargs):
        legislation_page = ''
        context = super().get_context_data(**kwargs)
        legislations = Legislation.objects.all().first()
        regulations = Regulations.objects.all()
        if SeoPages.objects.filter(page_name='legislation').exists():
            # print('zdesss')
            legislation_page = SeoPages.objects.get(page_name='legislation')
        lang = self.request.GET.get('lang')
        if lang:
            legislations.language(lang).all().first()
            regulations.language(lang).all()
        context['legislations'] = legislations
        context['legislation_page'] = legislation_page
        context['regulations'] = regulations
        return context
