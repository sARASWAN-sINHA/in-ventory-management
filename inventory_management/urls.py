"""
URL configuration for inventory_management project.

"""
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView



djoser_urls = [
    path('', include('djoser.urls')),
    path('login/', include('djoser.urls.jwt')),
]

swagger_urls = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

app_urls = [
    path('profile/', include('userprofile.urls')),
]

urlpatterns = [path('admin/', admin.site.urls)] + \
            djoser_urls + \
            swagger_urls + \
            app_urls
