"""
Конфигурация URL для проекта recipe_site.

Этот модуль определяет основные URL-маршруты проекта:
- Административный интерфейс (/admin/)
- Документация админки (/admin/doc/)
- Все URL приложения рецептов (/)

Также настраивается обработка медиа-файлов в режиме разработки.

Подробнее о настройке URL в Django:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from fastapi.middleware.wsgi import WSGIMiddleware
from api.main import app as fastapi_app

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('api/', WSGIMiddleware(fastapi_app)),  # FastAPI под /api/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)