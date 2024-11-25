"""
Конфигурация приложения рецептов.

Этот модуль определяет основные настройки Django-приложения для работы с рецептами,
включая имя приложения и настройки автоматического поля первичного ключа.
"""

from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """
    Класс конфигурации приложения рецептов.
    
    Attributes:
        default_auto_field (str): Тип поля для автоматически создаваемых
                                 первичных ключей моделей.
        name (str): Имя приложения, используемое Django для идентификации.
        verbose_name (str): Человекочитаемое название приложения для админ-панели.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
    verbose_name = 'Рецепты'
