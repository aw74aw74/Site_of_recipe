"""
Конфигурация URL для приложения рецептов.

Этот модуль определяет все URL-маршруты для приложения, включая:
- Просмотр, создание, редактирование и удаление рецептов
- Аутентификацию пользователей (регистрация, вход, выход)
- Управление категориями
"""

from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', 
         views.home, 
         name='home',
         # Главная страница со списком рецептов
    ),
    
    # Управление рецептами
    path('recipe/<int:recipe_id>/', 
         views.recipe_detail, 
         name='recipe_detail',
         # Детальная страница рецепта, recipe_id - идентификатор рецепта
    ),
    path('recipe/add/', 
         views.add_recipe, 
         name='add_recipe',
         # Страница создания нового рецепта
    ),
    path('recipe/<int:recipe_id>/edit/', 
         views.edit_recipe, 
         name='edit_recipe',
         # Страница редактирования рецепта, recipe_id - идентификатор рецепта
    ),
    path('recipe/<int:recipe_id>/delete/', 
         views.delete_recipe, 
         name='delete_recipe',
         # URL для удаления рецепта, recipe_id - идентификатор рецепта
    ),
    
    # Аутентификация пользователей
    path('signup/', 
         views.signup, 
         name='signup',
         # Страница регистрации нового пользователя
    ),
    path('login/', 
         views.login_view, 
         name='login',
         # Страница входа в систему
    ),
    path('logout/', 
         views.logout_view, 
         name='logout',
         # URL для выхода из системы
    ),
    
    # Управление категориями
    path('category/add/', 
         views.add_category_ajax, 
         name='add_category'),
]
