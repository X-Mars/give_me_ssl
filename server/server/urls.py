"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from apps.certificates.urls import router as cert_router
from apps.providers.urls import router as providers_router
from apps.notifications.urls import router as notifications_router
from apps.system_settings.urls import router as system_router

API_PREFIX = 'api/v1/'

api_router = DefaultRouter()
api_router.registry.extend(cert_router.registry)
api_router.registry.extend(providers_router.registry)
api_router.registry.extend(notifications_router.registry)
api_router.registry.extend(system_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{API_PREFIX}auth/', include('apps.accounts.urls')),
    path(f'{API_PREFIX}', include(api_router.urls)),
]

