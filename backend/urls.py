"""
URL configuration for backend project.

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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.views.generic import TemplateView
import os

from users.views import UserViewSet
from education.views import (
    ProgramViewSet, AccreditationViewSet,
    PublicationViewSet, MobilityProgramViewSet
)

# Роутер API
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'accreditations', AccreditationViewSet)
router.register(r'publications', PublicationViewSet)
router.register(r'mobility-programs', MobilityProgramViewSet)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('admin/', admin.site.urls),
    
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    path('api/register-university/', UserViewSet.as_view({'post': 'register_university'}), name='register-university'),
    path('api/users/login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('api/csrf/', get_csrf_token, name='csrf'),
]

# Медиа-файлы только для разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Добавляем маршрут для обслуживания файлов из директории assets напрямую
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR, 'backend', 'static', 'assets'))
    # Добавляем маршрут для обслуживания файла vite.svg напрямую
    urlpatterns += static('/vite.svg', document_root=os.path.join(settings.BASE_DIR, 'backend', 'static'))
