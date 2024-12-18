import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Остальной код
