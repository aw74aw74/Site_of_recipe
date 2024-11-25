from django.contrib import admin
from .models import Recipe, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'preparation_time')
    search_fields = ('title', 'description', 'steps')
    list_filter = ('categories', 'author')
    ordering = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
