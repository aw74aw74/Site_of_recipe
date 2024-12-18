"""
ASGI config for recipe_site project.
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.routing import Mount
from api.main import app as fastapi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_site.settings')
django_app = get_asgi_application()

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавляем маршруты FastAPI
for route in fastapi_app.routes:
    if route.path != "/":  # Пропускаем корневой маршрут FastAPI
        app.routes.append(route)

# Добавляем Django как корневое приложение
app.mount("/", django_app)

# Экспортируем приложение
application = app
