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
    created_at: datetime
    updated_at: datetime
    categories: List[Category] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
