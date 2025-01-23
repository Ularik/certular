from django.views.generic import TemplateView

from appeals_app.forms import AddAppealForm
from .models import Contacts
from main_app.models import SeoPages


class ContactsDetailView(TemplateView):
    template_name = 'contacts/contacts_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact = Contacts.objects.first()
        contacts_page = ''
        if SeoPages.objects.filter(page_name='contacts').exists():
            # print('zdesss')
            contacts_page = SeoPages.objects.get(page_name='contacts')
        lang = self.request.GET.get('lang')
        form = AddAppealForm()
        if lang:
            contact.language(lang).all()
        context['contact'] = contact
        context['contacts_page'] = contacts_page
        context['form'] = form
        return context
