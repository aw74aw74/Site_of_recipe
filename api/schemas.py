from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

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
    title: str
    description: str
    cooking_time: int

class RecipeCreate(RecipeBase):
    categories: Optional[List[int]] = None

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cooking_time: Optional[int] = None
    categories: Optional[List[int]] = None

class Recipe(RecipeBase):
    id: int
    image: Optional[str] = None
    author: User
    categories: List[Category] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # Преобразуем ImageFieldFile в строку
        if obj.image:
            obj.image = str(obj.image)
        # Преобразуем related manager в список
        obj.categories = list(obj.categories.all())
        return super().from_orm(obj)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
