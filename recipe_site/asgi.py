"""
ASGI config for recipe_site project.
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.middleware.wsgi import WSGIMiddleware
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

# Маршрутизация для FastAPI документации
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Recipe API Documentation"
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    return get_openapi(
        title="Recipe API",
        version="1.0.0",
        description="API для управления рецептами",
        routes=fastapi_app.routes
    )

# Монтируем Django как корневой маршрут
app.mount("/", WSGIMiddleware(django_app))

# Монтируем FastAPI маршруты
for route in fastapi_app.routes:
    app.routes.append(route)

# Экспортируем приложение
application = app
