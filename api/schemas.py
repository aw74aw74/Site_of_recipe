from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class RecipeBase(BaseModel):
    title: str
    description: str
    ingredients: str
    steps: str
    preparation_time: int

class RecipeCreate(RecipeBase):
    category_ids: List[int]

class RecipeUpdate(RecipeBase):
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[str] = None
    steps: Optional[str] = None
    preparation_time: Optional[int] = None
    category_ids: Optional[List[int]] = None

class Recipe(RecipeBase):
    id: int
    image: Optional[str] = None
    author_id: int
    created_at: datetime
    updated_at: datetime
    categories: List[Category]

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
