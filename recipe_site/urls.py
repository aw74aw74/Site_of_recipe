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

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
]

# Добавляем обработку медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)