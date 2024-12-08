from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Таблица связи между рецептами и категориями
recipe_category = Table(
    'recipes_recipe_categories',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes_recipe.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('recipes_category.id'), primary_key=True)
)

class Category(Base):
    __tablename__ = 'recipes_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    recipes = relationship('Recipe', secondary=recipe_category, back_populates='categories')

    def __repr__(self):
        return f"<Category {self.name}>"

class Recipe(Base):
    __tablename__ = 'recipes_recipe'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    ingredients = Column(Text)
    steps = Column(Text)
    preparation_time = Column(Integer)
    image = Column(String(100), nullable=True)
    author_id = Column(Integer, ForeignKey('auth_user.id'))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    categories = relationship('Category', secondary=recipe_category, back_populates='recipes')
    author = relationship('User')

    def __repr__(self):
        return f"<Recipe {self.title}>"

class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_login = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"
