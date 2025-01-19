from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('main_app.urls')),
    path('about/', include('about_app.urls')),
    path("admin/", admin.site.urls),
]

# tinymce module include
urlpatterns += [
    path('tinymce/', include('tinymce.urls')),
]