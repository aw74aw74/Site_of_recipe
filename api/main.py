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

# Dependency
def get_db():
    # db = SessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()
    pass

# Инициализация базовой аутентификации
security = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(credentials: OAuth2PasswordRequestForm = Depends(), db = None):
    """Проверка логина и пароля пользователя"""
    # user = db.query(models.User).filter(models.User.username == credentials.username).first()
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Неверное имя пользователя",
    #         headers={"WWW-Authenticate": "Basic"},
    #     )
    
    # # Для простоты тестирования проверяем, что пароль совпадает с именем пользователя
    # if credentials.password != credentials.username:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Неверный пароль",
    #         headers={"WWW-Authenticate": "Basic"},
    #     )
    
    # return user
    pass

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = None
):
    """Получение токена доступа"""
    # user = auth.authenticate_user(db, form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = auth.create_access_token(
    #     data={"sub": user.username}, expires_delta=access_token_expires
    # )
    # return {"access_token": access_token, "token_type": "bearer"}
    pass

@app.get("/recipes/", response_model=List[schemas.Recipe])
def read_recipes(skip: int = 0, limit: int = 100, db = None):
    """Получение списка всех рецептов"""
    # recipes = db.query(models.Recipe).offset(skip).limit(limit).all()
    # return recipes
    pass

@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(recipe_id: int, db = None):
    """Получение рецепта по ID"""
    # recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    # if recipe is None:
    #     raise HTTPException(status_code=404, detail="Рецепт не найден")
    # return recipe
    pass

@app.post("/recipes/", response_model=schemas.Recipe)
async def create_recipe(
    recipe: schemas.RecipeCreate,
    image: UploadFile = File(...),
    db = None,
    current_user = None
):
    """
    Создание нового рецепта.
    Требует аутентификации пользователя.
    """
    # # Загружаем изображение в Cloudinary
    # cloudinary_response = cloudinary.uploader.upload(image.file)
    # db_recipe = models.Recipe(
    #     title=recipe.title,
    #     description=recipe.description,
    #     ingredients=recipe.ingredients,
    #     steps=recipe.steps,
    #     preparation_time=recipe.preparation_time,
    #     image=cloudinary_response['secure_url'],  # Сохраняем URL изображения
    #     author_id=current_user.id
    # )
    
    # # Добавляем категории
    # categories = db.query(models.Category).filter(
    #     models.Category.id.in_(recipe.category_ids)
    # ).all()
    # db_recipe.categories = categories
    
    # db.add(db_recipe)
    # db.commit()
    # db.refresh(db_recipe)
    # return db_recipe
    pass

@app.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(
    recipe_id: int,
    recipe: schemas.RecipeUpdate,
    db = None,
    current_user = None
):
    """
    Обновление рецепта.
    Требует аутентификации пользователя.
    Пользователь может обновлять только свои рецепты.
    """
    # db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    # if db_recipe is None:
    #     raise HTTPException(status_code=404, detail="Рецепт не найден")
    
    # # Проверяем, что пользователь является автором рецепта
    # if db_recipe.author_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Нет прав для обновления этого рецепта"
    #     )

    # # Обновляем поля рецепта
    # if recipe.title is not None:
    #     db_recipe.title = recipe.title
    # if recipe.description is not None:
    #     db_recipe.description = recipe.description
    # if recipe.ingredients is not None:
    #     db_recipe.ingredients = recipe.ingredients
    # if recipe.steps is not None:
    #     db_recipe.steps = recipe.steps
    # if recipe.preparation_time is not None:
    #     db_recipe.preparation_time = recipe.preparation_time
    
    # # Обновляем категории, если они предоставлены
    # if recipe.category_ids is not None:
    #     categories = db.query(models.Category).filter(
    #         models.Category.id.in_(recipe.category_ids)
    #     ).all()
    #     db_recipe.categories = categories

    # db.commit()
    # db.refresh(db_recipe)
    # return db_recipe
    pass

@app.delete("/recipes/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db = None,
    current_user = None
):
    """
    Удаление рецепта.
    Требует аутентификации пользователя.
    Пользователь может удалить только свой рецепт.
    """
    # db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    # if db_recipe is None:
    #     raise HTTPException(status_code=404, detail="Рецепт не найден")
    
    # # Проверяем, что пользователь является автором рецепта
    # if db_recipe.author_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Нет прав для удаления этого рецепта"
    #     )
    
    # db.delete(db_recipe)
    # db.commit()
    
    # return {"message": f"Рецепт {recipe_id} успешно удален"}
    pass

@app.put("/recipes/{recipe_id}/image", response_model=schemas.Recipe)
async def update_recipe_image(
    recipe_id: int,
    image: UploadFile = File(...),
    db = None,
    current_user = None
):
    """Обновление изображения рецепта"""
    # recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    # if not recipe:
    #     raise HTTPException(status_code=404, detail="Рецепт не найден")
    
    # # Проверяем, что пользователь является автором рецепта
    # if recipe.author_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Нет прав для обновления этого рецепта"
    #     )
    
    # # Загружаем изображение в Cloudinary
    # cloudinary_response = cloudinary.uploader.upload(image.file)
    # recipe.image = cloudinary_response['secure_url']  # Сохраняем URL изображения
    
    # db.commit()
    # db.refresh(recipe)

    # return recipe
    pass

@app.get("/categories/", response_model=List[schemas.Category])
def get_categories(db = None):
    """Получение списка всех категорий"""
    # return db.query(models.Category).all()
    pass

@app.get("/categories/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db = None):
    """Получение конкретной категории по ID"""
    # category = db.query(models.Category).filter(models.Category.id == category_id).first()
    # if category is None:
    #     raise HTTPException(status_code=404, detail="Категория не найдена")
    # return category
    pass

@app.get("/")
async def read_root():
    return {"message": "Welcome to Recipe API"}
