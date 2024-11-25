"""
Представления (views) для приложения рецептов.

Этот модуль содержит все представления, необходимые для работы с рецептами:
- отображение списка рецептов
- детальный просмотр рецепта
- создание нового рецепта
- редактирование существующего рецепта
- удаление рецепта
- фильтрация рецептов по категориям

Каждое представление включает в себя необходимые проверки прав доступа
и обработку данных форм.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe, Category
from .forms import RecipeForm, CategoryFilterForm
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    """
    Отображает главную страницу со списком всех рецептов.
    
    Аргументы:
        request: объект HttpRequest
    
    Возвращает:
        HttpResponse с отрендеренным шаблоном home.html
        
    Особенности:
        - Поддерживает фильтрацию по категориям
        - Отображает все рецепты, если фильтры не выбраны
        - Сохраняет выбранные фильтры в форме
        - Сортирует рецепты по названию в алфавитном порядке
    """
    # Инициализация формы фильтрации
    form = CategoryFilterForm(request.GET)
    recipes = Recipe.objects.all().order_by('title')  # Добавляем сортировку по названию
    selected_categories = []

    # Применение фильтров, если они выбраны
    if form.is_valid() and form.cleaned_data['categories']:
        selected_categories = form.cleaned_data['categories']
        recipes = recipes.filter(categories__in=selected_categories).distinct().order_by('title')  # Сохраняем сортировку после фильтрации

    context = {
        'recipes': recipes,
        'form': form,
        'selected_categories': selected_categories
    }
    return render(request, 'recipes/home.html', context)

def recipe_detail(request, recipe_id):
    """
    Отображает детальную страницу рецепта.
    
    Args:
        request: объект HttpRequest
        recipe_id: идентификатор рецепта
        
    Returns:
        HttpResponse с отрендеренным шаблоном
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def add_recipe(request):
    """
    Обрабатывает создание нового рецепта.
    
    Аргументы:
        request: объект HttpRequest
    
    Возвращает:
        - При GET: форму создания рецепта
        - При успешном POST: перенаправление на страницу рецепта
        - При ошибке в POST: форму с ошибками
        
    Требования:
        - Пользователь должен быть аутентифицирован
        - Форма должна быть валидной
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()  # Сохраняем связи many-to-many
            messages.success(request, 'Рецепт успешно добавлен!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Добавить рецепт'})

@login_required
def edit_recipe(request, recipe_id):
    """
    Редактирование существующего рецепта.
    
    Args:
        request: объект HttpRequest
        recipe_id: идентификатор рецепта
        
    Returns:
        HttpResponse с отрендеренным шаблоном или редирект
    """
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Рецепт успешно обновлен!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Редактировать рецепт'
    })

@login_required
def delete_recipe(request, recipe_id):
    """
    Удаление рецепта.
    
    Args:
        request: объект HttpRequest
        recipe_id: идентификатор рецепта
        
    Returns:
        HttpResponse редирект на главную страницу
    """
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    recipe.delete()
    messages.success(request, 'Рецепт успешно удален!')
    return redirect('home')

def signup(request):
    """
    Регистрирует нового пользователя в системе.

    Args:
        request (HttpRequest): Объект запроса Django.

    Returns:
        HttpResponse: При GET - форма регистрации.
                     При успешном POST - редирект на главную страницу
                     с автоматическим входом пользователя.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    """
    Аутентифицирует пользователя в системе.

    Args:
        request (HttpRequest): Объект запроса Django.

    Returns:
        HttpResponse: При GET - форма входа.
                     При успешном POST - редирект на главную страницу.

    Notes:
        Использует встроенную форму аутентификации Django.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def add_category(request):
    """
    Добавляет новую категорию рецептов. Требует аутентификации пользователя.

    Args:
        request (HttpRequest): Объект запроса Django.

    Returns:
        HttpResponse: При GET - форма создания категории.
                     При успешном POST - редирект на главную страницу.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'recipes/add_category.html', {'form': form})

def add_category_ajax(request):
    """
    Представление для добавления новой категории через AJAX.
    
    Args:
        request: объект HttpRequest
        
    Returns:
        JsonResponse с результатом операции
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            try:
                # Создаем новую категорию
                category = Category.objects.create(name=name)
                return JsonResponse({
                    'success': True,
                    'category': {
                        'id': category.id,
                        'name': category.name
                    }
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Название категории не может быть пустым'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Метод не поддерживается'
    })

def logout_view(request):
    """
    Выход пользователя из системы.

    Args:
        request (HttpRequest): Объект запроса Django.

    Returns:
        HttpResponse: Редирект на главную страницу после выхода.
    """
    logout(request)
    return redirect('home')
