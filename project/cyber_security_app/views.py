from django.views import generic
from django.views.generic import TemplateView

from .models import CyberSecurity


class CyberSecurityListView(TemplateView):
    template_name = 'legislation/legislation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.request.GET.get('lang')
        cyber_security = CyberSecurity.objects.all()
        if lang:
            cyber_security.language(lang).all()
        context['cyber_security'] = cyber_security
        return context


class CyberSecurityView(generic.DetailView):
    model = CyberSecurity
    context_object_name = 'cyber_security'
    template_name = 'cyber_security/cyber_security.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        # print(self.request.GET)
        lang = self.request.GET.get('lang')
        if lang:
            queryset.language(lang).all()
        # print(queryset)
        return queryset
