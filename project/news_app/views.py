from django.shortcuts import render
from django.views import generic

from main_app.models import SeoPages
from .models import News
from datetime import datetime, timedelta


class NewsListView(generic.ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'news/news_list.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('time'):
            the_time = datetime.now() - timedelta(days=int(self.request.GET.get('time')))
            queryset = queryset.filter(created_at__gte=the_time)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        news_page = ''
        if SeoPages.objects.filter(page_name='news').exists():
            news_page = SeoPages.objects.get(page_name='news')
        context['news_page'] = news_page
        return context


class NewsDetailView(generic.DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'news/news_detail.html'
