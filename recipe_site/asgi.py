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
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_site.settings')
django_app = get_asgi_application()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Добавляем Django как приложение на префиксе
app.mount("/django", django_app)

# Экспортируем приложение
application = app

# Логирование запросов
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Handling request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
