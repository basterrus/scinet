from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from mainapp import views as mainapp

urlpatterns = [
    path('', mainapp.section, name='index'),
    path('sections/', include('mainapp.urls', namespace='sections')),
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls', namespace='auth')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
