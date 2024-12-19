import pytest
import os
import django
from django.core.management import call_command

# Настройка Django для тестов
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_site.settings')
django.setup()

@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    """Настройка тестовой базы данных"""
    with django_db_blocker.unblock():
        # Создаем тестовую базу данных и применяем миграции
        call_command('migrate')
