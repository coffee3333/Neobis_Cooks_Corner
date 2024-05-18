from django.contrib import admin
from cooks_corner.models import Category, Ingredient, Recipe, SavedRecipe, LikedRecipe, Follow


admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(SavedRecipe)
admin.site.register(LikedRecipe)
admin.site.register(Follow)