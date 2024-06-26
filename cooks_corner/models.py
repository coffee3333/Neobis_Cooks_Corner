from django.db import models
from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit_name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.quantity})"


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='recipes', on_delete=models.CASCADE)
    cook_time = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=20, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id'] 


class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipe_images/')

    def __str__(self):
        return f"Image for {self.recipe.title}"


class SavedRecipe(models.Model):
    user = models.ForeignKey(User, related_name='saved_recipes', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='saved_by', on_delete=models.CASCADE)
    saved_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.title}"


class LikedRecipe(models.Model):
    user = models.ForeignKey(User, related_name='liked_recipes', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='liked_by', on_delete=models.CASCADE)
    liked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} liked {self.recipe.title}"


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"