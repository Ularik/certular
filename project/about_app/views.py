from .models import About, CenterTasks
from django.views import generic
from django.views.generic import TemplateView


class AboutTypeView(generic.ListView):
    model = About
    context_object_name = 'about_list'
    template_name = 'main/about.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        # print(self.request.GET.get('type'))
        lang = self.request.GET.get('lang')
        if lang:
            queryset.language(lang).all()
        print(queryset)
        return queryset


class AboutDetailView(TemplateView):
    template_name = 'about/about_detail.html'

    def get_context_data(self, **kwargs):
        about_page = ''
        context = super().get_context_data(**kwargs)
        about = About.objects.first()
        center_tasks = CenterTasks.objects.all()
        lang = self.request.GET.get('lang')
        if lang:
            about.language(lang).all()
            center_tasks.language(lang).all()
        context['about'] = about
        context['about_page'] = about_page
        context['center_tasks'] = center_tasks
        return context