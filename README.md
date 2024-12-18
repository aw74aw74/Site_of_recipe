# Сайт рецептов блюд

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
- Django 5.0
- FastAPI
- PostgreSQL
- HTML/CSS
- Bootstrap 5

## Установка и запуск на локальной машине

1. **Клонируйте репозиторий**
   ```bash
   git clone <your-repository-url>
   cd recipe_site
   ```

2. **Создайте виртуальное окружение и активируйте его**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # для Windows
   # source .venv/bin/activate  # для Linux/Mac
   ```

3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения**
   Создайте файл `.env` в корневой директории проекта со следующим содержимым:
   ```plaintext
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=.herokuapp.com,localhost,127.0.0.1
   DATABASE_URL=postgresql://postgres:postgres@localhost/db_postgresql
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

5. **Создайте базу данных PostgreSQL**
   ```sql
   psql -U postgres
   CREATE DATABASE db_postgresql;
   ```

6. **Примените миграции**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Создайте суперпользователя**
   ```bash
   python manage.py createsuperuser
   ```

8. **Запустите сервер разработки**
   ```bash
   python manage.py runserver
   ```

9. **Запустите FastAPI (в отдельном терминале)**
   ```bash
   uvicorn api.main:app --reload --port 8001
   ```

## Использование

- Django админ-панель: http://localhost:8000/admin/
- API документация: http://localhost:8001/docs
- Основной сайт: http://localhost:8000/

## API Endpoints

- `GET /api/recipes/` - Получить список всех рецептов
- `POST /api/recipes/` - Создать новый рецепт
- `GET /api/recipes/{id}/` - Получить рецепт по ID
- `PUT /api/recipes/{id}/` - Обновить рецепт
- `DELETE /api/recipes/{id}/` - Удалить рецепт
- `GET /api/categories/` - Получить список категорий

## Технологии

- Django
- FastAPI
- PostgreSQL
- Cloudinary
- JWT для аутентификации
- Swagger/OpenAPI для документации API

## Развертывание на Heroku

1. **Установите Heroku CLI и войдите в аккаунт**
   ```bash
   heroku login
   ```

2. **Создайте новое приложение на Heroku**
   ```bash
   heroku create your-app-name
   ```

3. **Добавьте базу данных PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Настройте переменные окружения на Heroku**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name
   heroku config:set CLOUDINARY_API_KEY=your-api-key
   heroku config:set CLOUDINARY_API_SECRET=your-api-secret
   ```

5. **Отправьте код на Heroku**
   ```bash
   git push heroku main
   ```

6. **Выполните миграции**
   ```bash
   heroku run python manage.py migrate
   ```

7. **Создайте суперпользователя**
   ```bash
   heroku run python manage.py createsuperuser
   ```

Приложение доступно по адресу: https://site-of-recipe-8841f2545ad5.herokuapp.com/

## API Интерфейс

API доступен по базовому URL: https://site-of-recipe-8841f2545ad5.herokuapp.com/api/

Документация API (Swagger UI): https://site-of-recipe-8841f2545ad5.herokuapp.com/api/docs

#### Основные эндпоинты:

- `GET /api/recipes/` - получение списка рецептов
- `GET /api/recipes/{id}` - получение конкретного рецепта
- `POST /api/recipes/` - создание нового рецепта
- `PUT /api/recipes/{id}` - обновление рецепта
- `DELETE /api/recipes/{id}` - удаление рецепта
- `GET /api/categories/` - получение списка категорий
- `GET /api/categories/{id}` - получение конкретной категории

### Аутентификация

Для доступа к API с правами на изменение данных требуется аутентификация:

1. Получите токен доступа:
```http
POST /api/token
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

2. Используйте токен в заголовке Authorization:
```http
Authorization: Bearer your_access_token
```

## Хранение фотографий

В проекте используется облачный сервис Cloudinary для хранения и управления изображениями рецептов.

### Настройка Cloudinary

1. **Создайте аккаунт**
   - Зарегистрируйтесь на [Cloudinary](https://cloudinary.com/)
   - Получите данные для доступа к API (Cloud Name, API Key, API Secret)

2. **Настройте переменные окружения**
   ```plaintext
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

### Особенности работы с изображениями

1. **Загрузка изображений**
   - Изображения автоматически загружаются в Cloudinary при создании/обновлении рецепта
   - Поддерживаются форматы: JPG, PNG, GIF
   - Максимальный размер файла: 10MB

2. **Автоматическая оптимизация**
   - Автоматическое сжатие изображений
   - Создание различных размеров для разных устройств
   - Оптимизация качества и размера

3. **Удаление изображений**
   - При удалении рецепта изображение автоматически удаляется из Cloudinary
   - Реализована защита от "осиротевших" файлов
   - Используются Django сигналы для синхронизации

4. **Безопасность**
   - Защищенная передача файлов через HTTPS
   - Валидация типов файлов
   - Проверка размера файлов

### Пример использования в коде

```python
from cloudinary.models import CloudinaryField

class Recipe(models.Model):
    # ...
    image = CloudinaryField('image')
    # ...
```

## Структура проекта

```plaintext
recipe_site/
├── api/                    # FastAPI приложение
│   ├── main.py            # Основной файл FastAPI
│   ├── models.py          # Модели для API
│   ├── schemas.py         # Pydantic схемы
│   └── auth.py            # Аутентификация для API
├── recipe_site/           # Основной проект Django
│   ├── settings.py        # Настройки проекта
│   ├── urls.py           # Основные URL маршруты
│   └── wsgi.py           # WSGI конфигурация
├── recipes/              # Django приложение для рецептов
│   ├── models.py         # Модели Django
│   ├── views.py         # Представления
│   ├── admin.py         # Настройки админ-панели
│   └── templates/       # HTML шаблоны
├── static/              # Статические файлы (CSS, JS)
├── requirements.txt    # Зависимости проекта
├── Procfile           # Конфигурация для Heroku
├── runtime.txt        # Версия Python для Heroku
└── manage.py          # Утилита командной строки Django
```

### Основные компоненты

1. **API (FastAPI)**
   - Реализация REST API
   - JWT аутентификация
   - Swagger документация

2. **Веб-приложение (Django)**
   - Административная панель
   - Управление рецептами
   - Пользовательский интерфейс

3. **База данных**
   - PostgreSQL (продакшен)
   - Миграции Django

4. **Облачные сервисы**
   - Cloudinary для хранения изображений (все медиафайлы хранятся в облаке)
   - Heroku для хостинга

## Известные проблемы

- Изображения рецептов не сохраняются на Heroku из-за эфемерной файловой системы. В планах - интеграция с облачным хранилищем.

## Лицензия

MIT License
