"""
Конфигурация административного интерфейса.

Этот модуль определяет настройки отображения моделей в админ-панели Django,
включая списки отображаемых полей, поиск и фильтрацию.
"""

from django.contrib import admin
from .models import Recipe, Category


class CategoryAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Category в админ-панели.
    
    Attributes:
        list_display: Поля, отображаемые в списке категорий
        search_fields: Поля, по которым возможен поиск
        ordering: Сортировка категорий
    """
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Recipe в админ-панели.
    
    Attributes:
        list_display: Поля, отображаемые в списке рецептов
        search_fields: Поля, по которым возможен поиск
        list_filter: Поля для фильтрации рецептов
        ordering: Сортировка рецептов
    """
    list_display = ('title', 'author', 'preparation_time')
    search_fields = ('title', 'description', 'steps')
    list_filter = ('categories', 'author')
    ordering = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
