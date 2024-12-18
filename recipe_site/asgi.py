"""
ASGI config for recipe_site project.
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Монтируем FastAPI приложение на /api
app.mount("/api", fastapi_app)

# Монтируем Django приложение как корневое
app.mount("/", WSGIMiddleware(django_app))
