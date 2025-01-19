from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from about_app.models import About, CenterTasks
from cyber_security_app.models import CyberSecurity
from django.views import View


class MainIndex(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        about = About.objects.first()
        center_tasks = CenterTasks.objects.all()

        context['about'] = about
        context['center_tasks'] = center_tasks

        return context


class SearchIndex(View):
    template_name = 'main/search.html'

    def get(self, request, *args, **kwargs):
        query_dict = request.GET

        query = query_dict.get('search', None)

        context = {}
        if query:
            cyber_security = CyberSecurity.objects.filter(translations__name__icontains=query).distinct()
            # news = News.objects.filter(translations__name__icontains=query).distinct()
            # trainings = Trainings.objects.filter(translations__name__icontains=query).distinct()
            # regulations = Regulations.objects.filter(translations__description__icontains=query).distinct()

            context['cyber_security'] = cyber_security
            # context['news'] = news
            # context['trainings'] = trainings
            # context['regulations'] = regulations
        print(context)
        return render(request, 'main/search.html', context=context)
#
#
# class RobotTxtView(TemplateView):
#     template_name = 'main/robots.txt'
#     content_type = 'text/plain'
#
#
# class SitemapXmlView(TemplateView):
#     template_name = 'main/sitemap.html'
#     content_type = 'application/xml'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['news'] = News.objects.all()
#         context['cyber_security'] = CyberSecurity.objects.all()
#         context['about'] = About.objects.first()
#         context['trainings'] = Trainings.objects.all()
#         context['legislation'] = Legislation.objects.first()
#         return context
#
#
# def page_not_found_view(request, exception):
#     for lang_code, _ in settings.LANGUAGES:
#         if request.path.startswith('/' + lang_code):
#             return render(request, 'main/404.html')
#     lang_cookie = request.COOKIES.get('cookie_language_appname')
#     if lang_cookie:
#         return redirect('/' + lang_cookie + request.path)
#     else:
#         return redirect('/' + settings.LANGUAGE_CODE + request.path)

