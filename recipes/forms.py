"""
Формы для приложения рецептов.

Этот модуль содержит формы Django для работы с рецептами и категориями,
включая создание и редактирование рецептов, управление категориями
и фильтрацию рецептов по категориям.
"""

from django import forms
from .models import Recipe, Category

class RecipeForm(forms.ModelForm):
    """
    Форма для создания и редактирования рецептов.
    
    Attributes:
        Meta.model: Модель Recipe, с которой связана форма
        Meta.fields: Список полей модели для отображения в форме
        Meta.labels: Словарь с пользовательскими названиями полей
        Meta.widgets: Словарь с настройками виджетов для полей
    
    Fields:
        title: Название рецепта
        description: Краткое описание рецепта
        ingredients: Список ингредиентов
        steps: Пошаговые инструкции приготовления
        preparation_time: Время приготовления в минутах
        image: Фотография готового блюда
        categories: Связанные категории рецепта
    
    Notes:
        - Для текстовых полей используются виджеты Textarea с настроенным размером
        - Поле categories поддерживает множественный выбор категорий
    """
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'steps', 'preparation_time', 'image', 'categories']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'ingredients': 'Ингредиенты',
            'steps': 'Шаги приготовления',
            'preparation_time': 'Время приготовления (в минутах)',
            'image': 'Изображение',
            'categories': 'Категории',
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Краткое описание рецепта'
            }),
            'ingredients': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Введите каждый ингредиент с новой строки'
            }),
            'steps': forms.Textarea(attrs={
                'rows': 20,
                'cols': 60,
                'placeholder': 'Опишите пошагово процесс приготовления'
            }),
        }

    def clean_categories(self):
        """
        Валидация и обработка категорий рецепта.
        
        Returns:
            list: Список объектов Category, включая новые категории,
                  если они были добавлены.
        
        Notes:
            Автоматически создает новые категории, если они не существуют
            в базе данных.
        """
        categories = self.cleaned_data.get('categories', [])
        new_categories = []
        for category in categories:
            if not Category.objects.filter(name=category.name).exists():
                new_category = Category.objects.create(name=category.name)
                new_categories.append(new_category)
            else:
                new_categories.append(category)
        return new_categories


class CategoryForm(forms.ModelForm):
    """
    Форма для создания и редактирования категорий рецептов.
    
    Attributes:
        Meta.model: Модель Category, с которой связана форма
        Meta.fields: Список полей модели для отображения в форме
        Meta.labels: Словарь с пользовательскими названиями полей
    
    Fields:
        name: Название категории
    """
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Название',
        }


class CategoryFilterForm(forms.Form):
    """
    Форма для фильтрации рецептов по категориям.
    
    Attributes:
        categories: Поле множественного выбора категорий
    
    Fields:
        categories: ModelMultipleChoiceField для выбора нескольких категорий
    
    Notes:
        - Использует CheckboxSelectMultiple для удобного выбора категорий
        - Категории отсортированы по алфавиту
        - Поле не является обязательным
    """
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by('name'),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label=''
    )

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы.
        
        Настраивает отображение названий категорий в списке выбора.
        """
        super().__init__(*args, **kwargs)
        self.fields['categories'].label_from_instance = lambda obj: obj.name
