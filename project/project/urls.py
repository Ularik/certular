from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('main_app.urls')),
    path('accounts/', include('accounts_app.urls')),
    path('about/', include('about_app.urls')),
    path('news/', include('news_app.urls')),
    path('cyber_security/', include('cyber_security_app.urls')),
    path('contacts/', include('contacts_app.urls')),
    path('appeals/', include('appeals_app.urls')),
    path('legislation/', include('legislation_app.urls')),
    path('cooperation/', include('cooperation_app.urls')),
    path("admin/", admin.site.urls),
]

# tinymce module include
urlpatterns += [
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "main_app.views.page_not_found_view"
