"""
ASGI config for recipe_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from api.main import app as fastapi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_site.settings')

django_app = get_asgi_application()

app = FastAPI()

# Монтируем Django под корневым путем
app.mount("/", WSGIMiddleware(django_app))

# Монтируем FastAPI под путем /api
app.mount("/api", fastapi_app)

# Экспортируем приложение для Uvicorn
application = app
