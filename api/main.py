import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import cloudinary
import cloudinary.uploader
from io import BytesIO
from typing import List
from asgiref.sync import sync_to_async

# Настройка путей для Django
CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Инициализация Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_site.settings')
import django
django.setup()

# Импорты Django после инициализации
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from recipes.models import Recipe, Category
from . import models, schemas, auth

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

# Инициализация базовой аутентификации
security = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(form_data: OAuth2PasswordRequestForm):
    """Аутентификация пользователя"""
    try:
        user = auth.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверное имя пользователя или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        logger.error(f"Error in authenticate_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Получение токена доступа"""
    try:
        user = authenticate_user(form_data)
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error in login_for_access_token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера"
        )

@app.get("/recipes/", response_model=List[schemas.Recipe])
async def read_recipes(skip: int = 0, limit: int = 100):
    """Получение списка всех рецептов"""
    @sync_to_async
    def get_recipes():
        recipes = Recipe.objects.all()[skip:skip + limit]
        return [schemas.Recipe.model_validate(recipe) for recipe in recipes]
    
    return await get_recipes()

@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
async def get_recipe(recipe_id: int):
    """Получение рецепта по ID"""
    @sync_to_async
    def get_recipe_by_id():
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            return schemas.Recipe.model_validate(recipe)
        except Recipe.DoesNotExist:
            raise HTTPException(status_code=404, detail="Рецепт не найден")
    
    return await get_recipe_by_id()

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
    # Загрузка изображения в Cloudinary
    image_content = await image.read()
    cloudinary_response = cloudinary.uploader.upload(
        BytesIO(image_content),
        folder="recipes"
    )
    
    # Создание рецепта
    recipe_obj = Recipe.objects.create(
        title=recipe.title,
        description=recipe.description,
        preparation_time=recipe.cooking_time,
        ingredients=recipe.ingredients,
        steps=recipe.steps,
        image=cloudinary_response['url'],
        author=current_user
    )
    
    # Добавление категорий
    if recipe.categories:
        recipe_obj.categories.set(recipe.categories)
    
    return schemas.Recipe.from_orm(recipe_obj)

@app.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
async def update_recipe(
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
        recipe_obj = Recipe.objects.get(id=recipe_id)
        
        # Проверка прав доступа
        if recipe_obj.author != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет прав для редактирования этого рецепта"
            )
        
        # Обновление полей
        if recipe.title is not None:
            recipe_obj.title = recipe.title
        if recipe.description is not None:
            recipe_obj.description = recipe.description
        if recipe.cooking_time is not None:
            recipe_obj.preparation_time = recipe.cooking_time
        if recipe.ingredients is not None:
            recipe_obj.ingredients = recipe.ingredients
        if recipe.steps is not None:
            recipe_obj.steps = recipe.steps
        if recipe.categories is not None:
            recipe_obj.categories.set(recipe.categories)
        
        recipe_obj.save()
        return schemas.Recipe.from_orm(recipe_obj)
        
    except Recipe.DoesNotExist:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

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
async def get_categories():
    """Получение списка всех категорий"""
    @sync_to_async
    def get_all_categories():
        categories = Category.objects.all()
        return [schemas.Category.model_validate(category) for category in categories]
    
    return await get_all_categories()

@app.get("/categories/{category_id}", response_model=schemas.Category)
async def get_category(category_id: int):
    """Получение конкретной категории по ID"""
    @sync_to_async
    def get_category_by_id():
        try:
            category = Category.objects.get(id=category_id)
            return schemas.Category.model_validate(category)
        except Category.DoesNotExist:
            raise HTTPException(status_code=404, detail="Категория не найдена")
    
    return await get_category_by_id()

@app.get("/")
def read_root():
    """Корневой эндпоинт"""
    return {"message": "Добро пожаловать в API рецептов!"}
