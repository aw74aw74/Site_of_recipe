from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.models import CloudinaryField

class Category:
    def __init__(self, name):
        self.id = None
        self.name = name
        self.recipes = []

    def __repr__(self):
        return f"<Category {self.name}>"

class Recipe:
    def __init__(self, title, description, ingredients, steps, preparation_time, image, author_id):
        self.id = None
        self.title = title
        self.description = description
        self.ingredients = ingredients
        self.steps = steps
        self.preparation_time = preparation_time
        self.image = image  
        self.author_id = author_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.categories = []
        self.author = None

    def __repr__(self):
        return f"<Recipe {self.title}>"

class User:
    def __init__(self, username, password, email, first_name, last_name):
        self.id = None
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = True
        self.is_staff = False
        self.is_superuser = False
        self.date_joined = datetime.utcnow()
        self.last_login = None

    def __repr__(self):
        return f"<User {self.username}>"
