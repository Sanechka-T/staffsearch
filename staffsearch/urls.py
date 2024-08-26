"""
URL configuration for staffsearch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # URL для административного интерфейса
    path('', RedirectView.as_view(url='resumes', permanent=True), name='index'),  # Редирект на 'resumes'
    path('', include('resume.urls')),  # Включение URL-ов приложения 'resume'
    path('', include('services.urls')),  # Включение URL-ов приложения 'services'
    path('', include('vacancy.urls')),  # Включение URL-ов приложения 'vacancy'
    path('users/', include('users.urls', namespace='users')),  # Включение URL-ов приложения 'users' с пространством имен
    path('info/', include('info.urls', namespace='info')),  # Включение URL-ов приложения 'info' с пространством имен
    path('help/', include('help.urls', namespace='help')),  # Включение URL-ов приложения 'help' с пространством имен
    path('__debug__/', include("debug_toolbar.urls")),  # URL для панели отладки
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Настройка URL для медиафайлов
