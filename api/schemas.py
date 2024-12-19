from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj):
        # Преобразуем объект Django в словарь
        data = {
            "id": obj.id,
            "name": obj.name
        }
        return cls(**data)

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class RecipeBase(BaseModel):
    """Базовая схема для рецепта"""
    title: str
    description: str
    ingredients: str
    steps: str
    preparation_time: int

class RecipeCreate(RecipeBase):
    categories: Optional[List[int]] = None

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[str] = None
    steps: Optional[str] = None
    preparation_time: Optional[int] = None
    categories: Optional[List[int]] = None

class Recipe(RecipeBase):
    id: int
    author: str
    image: Optional[str] = None
    categories: list[Category] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj):
        # Преобразуем объект Django в словарь
        data = {
            "id": obj.id,
            "title": obj.title,
            "description": obj.description,
            "ingredients": obj.ingredients,
            "steps": obj.steps,
            "preparation_time": obj.preparation_time,
            "image": str(obj.image.url) if obj.image else None,
            "author": obj.author.username,
            "categories": [Category.model_validate(cat) for cat in obj.categories.all()],
            "created_at": obj.created_at,
            "updated_at": obj.updated_at
        }
        return cls(**data)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
