from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import List
from pathlib import Path
import logging
import shutil
import os
from . import models, schemas, auth
import cloudinary
import cloudinary.uploader
from django.core.wsgi import get_wsgi_application
from django.db import connection
from recipes.models import Recipe, Category
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание директории для медиафайлов если её нет
MEDIA_DIR = Path("media/recipes")
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Recipe API", 
             description="API для управления рецептами",
             version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_site.settings')
django_app = get_wsgi_application()

# Инициализация базовой аутентификации
security = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(credentials: OAuth2PasswordRequestForm = Depends()):
    """Проверка логина и пароля пользователя"""
    try:
        user = User.objects.get(username=credentials.username)
        if user.check_password(credentials.password):
            return user
    except User.DoesNotExist:
        pass
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверное имя пользователя или пароль",
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Получение токена доступа"""
    user = authenticate_user(form_data)
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/recipes/", response_model=List[schemas.Recipe])
def read_recipes(skip: int = 0, limit: int = 100):
    """Получение списка всех рецептов"""
    recipes = Recipe.objects.all()[skip:limit]
    return [schemas.Recipe.model_validate(recipe, from_attributes=True) for recipe in recipes]

@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(recipe_id: int):
    """Получение рецепта по ID"""
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        return schemas.Recipe.model_validate(recipe, from_attributes=True)
    except Recipe.DoesNotExist:
        raise HTTPException(status_code=404, detail="Recipe not found")

@app.post("/recipes/", response_model=schemas.Recipe)
async def create_recipe(
    recipe: schemas.RecipeCreate,
    image: UploadFile = File(...),
    current_user: User = Depends(auth.get_current_user)
):
    """
    Создание нового рецепта.
    Требует аутентификации пользователя.
    """
    try:
        # Загрузка изображения в Cloudinary
        image_data = await image.read()
        cloudinary_response = cloudinary.uploader.upload(image_data)
        image_url = cloudinary_response['secure_url']

        # Создание рецепта
        new_recipe = Recipe.objects.create(
            title=recipe.title,
            description=recipe.description,
            preparation_time=recipe.preparation_time,
            ingredients=recipe.ingredients,
            steps=recipe.steps,
            author=current_user,
            image=image_url
        )

        # Добавление категорий
        if recipe.categories:
            categories = Category.objects.filter(id__in=recipe.categories)
            new_recipe.categories.set(categories)

        return schemas.Recipe.model_validate(new_recipe, from_attributes=True)
    except Exception as e:
        logger.error(f"Error creating recipe: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(
    recipe_id: int,
    recipe: schemas.RecipeUpdate,
    current_user: User = Depends(auth.get_current_user)
):
    """
    Обновление рецепта.
    Требует аутентификации пользователя.
    Пользователь может обновлять только свои рецепты.
    """
    try:
        db_recipe = Recipe.objects.get(id=recipe_id)
        
        # Проверка прав доступа
        if db_recipe.author != current_user:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to update this recipe"
            )

        # Обновление полей
        if recipe.title is not None:
            db_recipe.title = recipe.title
        if recipe.description is not None:
            db_recipe.description = recipe.description
        if recipe.preparation_time is not None:
            db_recipe.preparation_time = recipe.preparation_time
        if recipe.ingredients is not None:
            db_recipe.ingredients = recipe.ingredients
        if recipe.steps is not None:
            db_recipe.steps = recipe.steps
        if recipe.categories is not None:
            categories = Category.objects.filter(id__in=recipe.categories)
            db_recipe.categories.set(categories)

        db_recipe.save()
        return schemas.Recipe.model_validate(db_recipe, from_attributes=True)
    except Recipe.DoesNotExist:
        raise HTTPException(status_code=404, detail="Recipe not found")
    except Exception as e:
        logger.error(f"Error updating recipe: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/recipes/{recipe_id}")
async def delete_recipe(
    recipe_id: int,
    current_user: User = Depends(auth.get_current_user)
):
    """
    Удаление рецепта.
    Требует аутентификации пользователя.
    Пользователь может удалить только свой рецепт.
    """
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        
        # Проверка прав доступа
        if recipe.author != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет прав для удаления этого рецепта"
            )
        
        recipe.delete()
        return {"message": "Рецепт успешно удален"}
        
    except Recipe.DoesNotExist:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

@app.put("/recipes/{recipe_id}/image")
async def update_recipe_image(
    recipe_id: int,
    image: UploadFile = File(...),
    current_user: User = Depends(auth.get_current_user)
):
    """Обновление изображения рецепта"""
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        
        # Проверка прав доступа
        if recipe.author != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет прав для обновления этого рецепта"
            )
        
        # Загрузка нового изображения в Cloudinary
        image_data = await image.read()
        cloudinary_response = cloudinary.uploader.upload(image_data)
        image_url = cloudinary_response['secure_url']
        
        recipe.image = image_url
        recipe.save()
        
        return {"message": "Изображение успешно обновлено"}
        
    except Recipe.DoesNotExist:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

@app.get("/categories/", response_model=List[schemas.Category])
def get_categories():
    """Получение списка всех категорий"""
    categories = Category.objects.all()
    return [schemas.Category.model_validate(category, from_attributes=True) for category in categories]

@app.get("/categories/{category_id}", response_model=schemas.Category)
def get_category(category_id: int):
    """Получение конкретной категории по ID"""
    try:
        category = Category.objects.get(id=category_id)
        return schemas.Category.model_validate(category, from_attributes=True)
    except Category.DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")

@app.get("/")
def read_root():
    """Корневой эндпоинт"""
    return {"message": "Добро пожаловать в API рецептов!"}
