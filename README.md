# Recipe Site

Веб-приложение для хранения и управления рецептами, разработанное с использованием Django и FastAPI.

## Особенности

- Создание, редактирование и удаление рецептов
- Загрузка изображений с использованием Cloudinary
- REST API с использованием FastAPI
- Аутентификация пользователей
- Адаптивный дизайн

## Структура проекта

```
recipe_site/
├── api/                    # FastAPI приложение
│   ├── __init__.py
│   ├── auth.py            # Аутентификация для API
│   ├── main.py            # Основные эндпоинты API
│   ├── schemas.py         # Pydantic модели
│
├── recipe_site/           # Основной проект Django
│   ├── __init__.py
│   ├── asgi.py           # ASGI конфигурация
│   ├── settings.py       # Настройки проекта
│   └── urls.py           # URL маршрутизация
│
├── recipes/               # Django приложение для рецептов
│   ├── migrations/       # Миграции базы данных
│   ├── static/          # Статические файлы
│   │   └── recipes/     # CSS, JavaScript, изображения
│   ├── templates/       # HTML шаблоны
│   │   └── recipes/    
│   ├── __init__.py
│   ├── admin.py        # Настройки админ-панели
│   ├── apps.py         # Конфигурация приложения
│   ├── forms.py        # Формы
│   ├── models.py       # Модели данных
│   ├── tests.py        # Тесты
│   ├── urls.py         # URL маршруты приложения
│   └── views.py        # Представления
│
├── static/             # Собранные статические файлы
├── .env              # Переменные окружения
├── .gitignore       # Игнорируемые файлы Git
├── Procfile         # Конфигурация для Heroku
├── README.md        # Документация проекта
├── requirements.txt # Зависимости Python
└── runtime.txt      # Версия Python для Heroku
```

## Технологии

- Python 3.10
- Django 5.0
- FastAPI
- PostgreSQL
- Cloudinary для хранения медиафайлов
- Bootstrap для фронтенда

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/recipe-site.git
cd recipe-site
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта:
```env
# Настройки Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Настройки Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Настройки базы данных для локальной разработки
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# Для SQLite (альтернативный вариант)
# DATABASE_URL=sqlite:///db.sqlite3
```

## Настройка базы данных

### Локальная разработка

Для локальной разработки вы можете использовать SQLite или PostgreSQL.

#### SQLite (простой вариант)
В файле `settings.py` уже настроено автоматическое определение базы данных. Для использования SQLite просто укажите в `.env`:
```env
DATABASE_URL=sqlite:///db.sqlite3
```

#### PostgreSQL (рекомендуется)
1. Установите PostgreSQL
2. Создайте базу данных:
```sql
CREATE DATABASE your_database_name;
```
3. Укажите URL базы данных в `.env`:
```env
DATABASE_URL=postgres://user:password@localhost:5432/your_database_name
```

### Heroku
Для Heroku база данных настраивается автоматически через переменные окружения. Heroku предоставляет `DATABASE_URL` автоматически при подключении PostgreSQL addon.

## Запуск

### Локально
1. Примените миграции:
```bash
python manage.py migrate
```

2. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

3. Запустите сервер:
```bash
uvicorn recipe_site.asgi:application --reload
```

Приложение будет доступно по адресу `http://localhost:8000`

### На Heroku
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## API Документация

API документация доступна по следующим адресам:
- Swagger UI: `/api/docs`
- ReDoc: `/api/redoc`

## Тестирование

### Запуск тестов на Heroku

1. Запустите тесты на Heroku:
```bash
heroku run pytest api/tests/test_api.py -v
```

2. Для просмотра покрытия кода тестами:
```bash
heroku run pytest api/tests/test_api.py -v --cov=api
```

Тесты проверяют:
- Аутентификацию и авторизацию
- CRUD операции с рецептами
- Работу с категориями
- Загрузку изображений
- Обработку ошибок

## Развертывание

### Настройка Heroku
1. Создайте приложение на Heroku
2. Добавьте PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:mini
```

3. Настройте переменные окружения:
```bash
heroku config:set SECRET_KEY=your_secret_key
heroku config:set CLOUDINARY_CLOUD_NAME=your_cloud_name
heroku config:set CLOUDINARY_API_KEY=your_api_key
heroku config:set CLOUDINARY_API_SECRET=your_api_secret
heroku config:set ALLOWED_HOSTS=.herokuapp.com
```

4. Разверните приложение:
```bash
git push heroku main
```

## Лицензия

MIT
