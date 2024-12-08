from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from . import models

# Получаем путь к базе данных
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/db.sqlite3"

# Создаем движок SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

# Функция-генератор для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
