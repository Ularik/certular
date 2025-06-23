from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from ninja import NinjaAPI
from reports_app.api import router as report_router

from django.contrib.auth.decorators import login_required
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer
from ninja_jwt.controller import NinjaJWTDefaultController



class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(
   title="API",
   description="Документация API",
    version="1.0",
    docs_decorator=login_required,
)
api.register_controllers(NinjaJWTDefaultController)


api.add_router("/router/", report_router)


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path('api/', api.urls, name='api'),
]

urlpatterns += i18n_patterns(
    path('', include('main_app.urls')),
    path('accounts/', include('accounts_app.urls')),
    path('messages/', include('messages_app.urls')),
    path('about/', include('about_app.urls')),
    path('news/', include('news_app.urls')),
    path('cyber_security/', include('cyber_security_app.urls')),
    path('contacts/', include('contacts_app.urls')),
    path('appeals/', include('appeals_app.urls')),
    path('legislation/', include('legislation_app.urls')),
    path('cooperation/', include('cooperation_app.urls')),
    path('reports/', include('reports_app.urls')),
    path('bulletins/', include('bulletins.urls'))
)

# tinymce module include
urlpatterns += [
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "main_app.views.page_not_found_view"
