from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home')
]
