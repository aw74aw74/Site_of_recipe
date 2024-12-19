import pytest
from fastapi.testclient import TestClient
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from api.main import app
import cloudinary
import os
from datetime import datetime

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Настройка тестового окружения перед каждым тестом"""
    # Настройка Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_site.settings')
    # Настройка Cloudinary для тестов
    cloudinary.config(
        cloud_name="test_cloud",
        api_key="test_key",
        api_secret="test_secret"
    )

@pytest.fixture
@pytest.mark.django_db
def test_user():
    """Создание тестового пользователя"""
    user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    return user

@pytest.fixture
@pytest.mark.django_db
def test_category():
    """Создание тестовой категории"""
    category = Category.objects.create(
        name='Test Category'
    )
    return category

@pytest.fixture
@pytest.mark.django_db
def test_recipe(test_user, test_category):
    """Создание тестового рецепта"""
    recipe = Recipe.objects.create(
        title='Test Recipe',
        description='Test Description',
        cooking_time=30,
        author=test_user,
        image='http://example.com/test.jpg'
    )
    recipe.categories.add(test_category)
    return recipe

@pytest.fixture
def auth_headers(test_user):
    """Получение заголовков с токеном авторизации"""
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_read_root():
    """Тест корневого эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Добро пожаловать в API рецептов!"}

@pytest.mark.django_db
def test_read_recipes():
    """Тест получения списка рецептов"""
    response = client.get("/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.django_db
def test_get_recipe(test_recipe):
    """Тест получения конкретного рецепта"""
    response = client.get(f"/recipes/{test_recipe.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Recipe"
    assert data["description"] == "Test Description"

@pytest.mark.django_db
def test_get_nonexistent_recipe():
    """Тест получения несуществующего рецепта"""
    response = client.get("/recipes/99999")
    assert response.status_code == 404

def test_create_recipe_unauthorized():
    """Тест создания рецепта без авторизации"""
    response = client.post(
        "/recipes/",
        json={
            "title": "New Recipe",
            "description": "New Description",
            "cooking_time": 45
        }
    )
    assert response.status_code == 401

@pytest.mark.django_db
def test_create_recipe(auth_headers, test_category, tmp_path):
    """Тест создания рецепта с авторизацией"""
    # Создаем временный файл для изображения
    test_image = tmp_path / "test.jpg"
    test_image.write_bytes(b"fake image content")
    
    with open(test_image, "rb") as image:
        response = client.post(
            "/recipes/",
            data={
                "title": "New Recipe",
                "description": "New Description",
                "cooking_time": 45,
                "categories": [test_category.id]
            },
            files={"image": ("test.jpg", image, "image/jpeg")},
            headers=auth_headers
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Recipe"
    assert data["description"] == "New Description"
    assert data["cooking_time"] == 45

@pytest.mark.django_db
def test_update_recipe(auth_headers, test_recipe):
    """Тест обновления рецепта"""
    response = client.put(
        f"/recipes/{test_recipe.id}",
        json={
            "title": "Updated Recipe",
            "description": "Updated Description",
            "cooking_time": 60
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Recipe"
    assert data["description"] == "Updated Description"
    assert data["cooking_time"] == 60

@pytest.mark.django_db
def test_update_recipe_unauthorized(test_recipe):
    """Тест обновления рецепта без авторизации"""
    response = client.put(
        f"/recipes/{test_recipe.id}",
        json={
            "title": "Updated Recipe",
            "description": "Updated Description",
            "cooking_time": 60
        }
    )
    assert response.status_code == 401

@pytest.mark.django_db
def test_delete_recipe(auth_headers, test_recipe):
    """Тест удаления рецепта"""
    response = client.delete(
        f"/recipes/{test_recipe.id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    
    # Проверяем, что рецепт действительно удален
    response = client.get(f"/recipes/{test_recipe.id}")
    assert response.status_code == 404

@pytest.mark.django_db
def test_delete_recipe_unauthorized(test_recipe):
    """Тест удаления рецепта без авторизации"""
    response = client.delete(f"/recipes/{test_recipe.id}")
    assert response.status_code == 401

@pytest.mark.django_db
def test_get_categories(test_category):
    """Тест получения списка категорий"""
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(category["name"] == "Test Category" for category in data)

@pytest.mark.django_db
def test_get_category(test_category):
    """Тест получения конкретной категории"""
    response = client.get(f"/categories/{test_category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"

@pytest.mark.django_db
def test_get_nonexistent_category():
    """Тест получения несуществующей категории"""
    response = client.get("/categories/99999")
    assert response.status_code == 404
