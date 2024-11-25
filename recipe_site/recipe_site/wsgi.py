"""
WSGI config for recipe_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Путь к директории проекта
CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent

# Добавляем путь к проекту в sys.path
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Загружаем переменные окружения из файла .env
env_path = BASE_DIR / '.env'
load_dotenv(env_path)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_site.settings')

# Запуск приложения
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
