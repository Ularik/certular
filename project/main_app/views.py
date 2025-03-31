from django.http import JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from about_app.models import About, CenterTasks
from cyber_security_app.models import CyberSecurity
from news_app.models import News
from cooperation_app.models import Cooperation
from .models import SeoPages
from django.views import View
from accounts_app.models import Organization
from reports_app.models import Reports
from django.db.models import Count


class MainIndex(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        home_index = ''
        context = super().get_context_data(**kwargs)
        about = About.objects.first()
        center_tasks = CenterTasks.objects.all()
        cyber_security = CyberSecurity.objects.all()
        news = News.objects.all()[:3]
        cooperations = Cooperation.objects.all()
        cooperations_to_five = cooperations[:5]
        if SeoPages.objects.filter(page_name='home_page').exists():
            home_index = SeoPages.objects.get(page_name='home_page')

        context['about'] = about
        context['center_tasks'] = center_tasks
        context['cyber_security'] = cyber_security
        context['news'] = news
        context['home_index'] = home_index
        context['cooperations_to_five'] = cooperations_to_five
        context['cooperations'] = cooperations
        return context


class SearchIndex(View):
    template_name = 'main/search.html'

    def get(self, request, *args, **kwargs):
        query_dict = request.GET

        query = query_dict.get('search', None)

        context = {}
        if query:
            cyber_security = CyberSecurity.objects.filter(translations__name__icontains=query).distinct()
            news = News.objects.filter(translations__name__icontains=query).distinct()

            context['cyber_security'] = cyber_security
            context['news'] = news

        return render(request, 'main/search.html', context=context)


class RobotTxtView(TemplateView):
    template_name = 'main/robots.txt'
    content_type = 'text/plain'


def page_not_found_view(request, exception):
    for lang_code, _ in settings.LANGUAGES:
        if request.path.startswith('/' + lang_code):
            return render(request, 'main/404.html')
    lang_cookie = request.COOKIES.get('cookie_language_appname')
    if lang_cookie:
        return redirect('/' + lang_cookie + request.path)
    else:
        return redirect('/' + settings.LANGUAGE_CODE + request.path)


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_admin, login_url='/')
def chart_view(request):
    return render(request, "charts/chart.html")


def chart_data(request):
    list_of_month = (Reports.objects.values('created_date__month')
                     .distinct().order_by('created_date__month'))
    list_of_month = list(list_of_month)[-6:]

    organizations_list = list(Organization.objects.values('id', 'name'))

    data = {}

    for month in list_of_month:
        data[month['created_date__month']] = list(map(list, list(Reports.objects.filter(
            created_date__month=month['created_date__month'])
            .values_list('status', 'organization__name')
            .annotate(total=Count('id')))))
    return JsonResponse({'result': data, 'org_list': organizations_list})
