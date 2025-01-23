from django.views import generic
from .models import Cooperation
from main_app.models import SeoPages


class CooperationsListView(generic.ListView):
    model = Cooperation
    context_object_name = 'cooperations_list'
    template_name = 'cooperations/cooperation_list.html'
    # paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cooperations = Cooperation.objects.all()
        cooperation_page = ''
        if SeoPages.objects.filter(page_name='cooperation').exists():
            # print('zdesss')
            cooperation_page = SeoPages.objects.get(page_name='cooperation')
        context['cooperation_page'] = cooperation_page
        context['cooperations'] = cooperations
        # print('zdesssssssss')
        return context
