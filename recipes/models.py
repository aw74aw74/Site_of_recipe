"""
Модели для приложения рецептов.
Этот модуль содержит определения моделей Django для работы с рецептами и категориями.

Модели:
    - Category: Модель для хранения категорий рецептов
    - Recipe: Основная модель для хранения рецептов

Примечания:
    - Все поля имеют подробные help_text для административного интерфейса
    - Используются связи ForeignKey и ManyToManyField для связей между моделями
    - Настроены мета-классы для корректного отображения в админке
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import cloudinary
import cloudinary.uploader
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Category(models.Model):
    """
    Модель категории рецептов.
    
    Атрибуты:
        name (CharField): Название категории, максимальная длина 100 символов.
    
    Методы:
        __str__: Возвращает строковое представление категории.
    
    Мета:
        verbose_name: Человекочитаемое название модели в единственном числе
        verbose_name_plural: Человекочитаемое название модели во множественном числе
    """
    name = models.CharField(
        max_length=100,
        help_text="Введите название категории",
        verbose_name="Название категории"
    )

    def __str__(self):
        """Возвращает строковое представление объекта Category."""
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']  # Сортировка по имени

class Recipe(models.Model):
    """
    Модель рецепта.
    
    Атрибуты:
        title (CharField): Название рецепта, максимальная длина 200 символов
        description (TextField): Описание рецепта
        ingredients (TextField): Список ингредиентов
        steps (TextField): Пошаговые инструкции приготовления
        preparation_time (IntegerField): Время приготовления в минутах
        image (ImageField): Фотография готового блюда
        author (ForeignKey): Ссылка на пользователя-автора рецепта
        categories (ManyToManyField): Связь с категориями рецепта
        created_at (DateTimeField): Дата и время создания рецепта
        updated_at (DateTimeField): Дата и время последнего обновления рецепта
    
    Методы:
        __str__: Возвращает строковое представление рецепта
        save: Переопределенный метод сохранения для обновления даты изменения
    """
    title = models.CharField(
        max_length=200,
        help_text="Введите название рецепта",
        verbose_name="Название"
    )
    
    description = models.TextField(
        help_text="Добавьте краткое описание рецепта",
        verbose_name="Описание"
    )
    
    ingredients = models.TextField(
        help_text="Перечислите ингредиенты, каждый с новой строки",
        verbose_name="Ингредиенты"
    )
    
    steps = models.TextField(
        help_text="Опишите процесс приготовления пошагово",
        verbose_name="Шаги приготовления"
    )
    
    preparation_time = models.IntegerField(
        help_text="Укажите время приготовления в минутах",
        verbose_name="Время приготовления"
    )
    
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=True,
        help_text="Загрузите фотографию готового блюда",
        verbose_name="Фотография"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Выберите автора рецепта",
        verbose_name="Автор"
    )
    
    categories = models.ManyToManyField(
        Category,
        help_text="Выберите категории для рецепта",
        verbose_name="Категории"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        """Возвращает строковое представление рецепта."""
        return f"{self.title} (автор: {self.author.username})"
    
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']  # Сортировка по дате создания (сначала новые)

@receiver(pre_delete, sender=Recipe)
def delete_recipe_image(sender, instance, **kwargs):
    """
    Сигнал для удаления изображения из Cloudinary перед удалением рецепта
    """
    if instance.image:  # Проверяем, есть ли изображение
        try:
            # Получаем public_id изображения из URL
            public_id = instance.image.public_id
            # Удаляем изображение из Cloudinary
            cloudinary.uploader.destroy(public_id)
        except Exception as e:
            print(f"Ошибка при удалении изображения из Cloudinary: {e}")
