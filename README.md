# Recipe Site

Веб-приложение для управления рецептами блюд с API интерфейсом.

## Описание

Приложение позволяет пользователям создавать, просматривать, редактировать и удалять рецепты блюд. Каждый рецепт содержит название, описание, ингредиенты, шаги приготовления, время приготовления и фотографию. Рецепты можно категоризировать по типам блюд.

## Основные возможности

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление рецептов
- Загрузка фотографий для рецептов
- Категоризация рецептов
- REST API для доступа к рецептам

## Технологии

- Python 3.10
- Django 4.2
- FastAPI
- PostgreSQL (в продакшене)
- SQLite (для разработки)
- HTML/CSS
- Bootstrap 5

## Установка и запуск локально

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd recipe-site
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv .venv
.venv\Scripts\activate  # для Windows
source .venv/bin/activate  # для Linux/Mac
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Запустите сервер:
```bash
python manage.py runserver
```

## Развертывание на Heroku

Приложение доступно по адресу: https://site-of-recipe-8841f2545ad5.herokuapp.com/

### Использование API

API доступен по базовому URL: https://site-of-recipe-8841f2545ad5.herokuapp.com/api/

Доступные эндпоинты:

#### Получение списка рецептов
```http
GET /api/recipes/
```

#### Получение конкретного рецепта
```http
GET /api/recipes/{recipe_id}/
```

#### Создание нового рецепта
```http
POST /api/recipes/
Content-Type: application/json

{
    "title": "Название рецепта",
    "description": "Описание рецепта",
    "ingredients": "Список ингредиентов",
    "steps": "Шаги приготовления",
    "preparation_time": "30 минут",
    "categories": [1, 2]
}
```

#### Обновление рецепта
```http
PUT /api/recipes/{recipe_id}/
Content-Type: application/json

{
    "title": "Новое название",
    ...
}
```

#### Удаление рецепта
```http
DELETE /api/recipes/{recipe_id}/
```

### Аутентификация в API

Для доступа к API требуется аутентификация. Используйте Basic Auth с вашими учетными данными от сайта.

## Структура проекта

- `recipe_site/` - основной проект Django
- `recipes/` - приложение Django для управления рецептами
- `api/` - FastAPI приложение для REST API
- `media/` - папка для хранения загруженных изображений
- `static/` - статические файлы (CSS, JavaScript)
- `templates/` - шаблоны HTML

## Лицензия

MIT License
