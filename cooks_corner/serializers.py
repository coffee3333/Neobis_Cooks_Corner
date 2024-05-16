from rest_framework import serializers
from cooks_corner.models import Recipe, Ingredient, Category, LikedRecipe, SavedRecipe
from rest_framework.exceptions import ValidationError
from django.db import transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class LikedRecipeListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = LikedRecipe
        fields = ['id', 'user', 'recipe', 'liked_on']
        read_only_fields = ['liked_on']


class LikedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedRecipe
        fields = ['id', 'recipe', 'liked_on']
        read_only_fields = ['liked_on']


class SavedRecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedRecipe
        fields = ['id', 'user', 'recipe', 'saved_on']
        read_only_fields = ['saved_on']


class SavedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedRecipe
        fields = ['id', 'recipe', 'saved_on']
        read_only_fields = ['saved_on']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity', 'quantity_name']


class RecipeListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    saves_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'author', 'category', 'image', 'likes_count', 'saves_count']

    def get_likes_count(self, obj):
        return LikedRecipe.objects.filter(recipe=obj).count()

    def get_saves_count(self, obj):
        return SavedRecipe.objects.filter(recipe=obj).count()


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    likes_count = serializers.SerializerMethodField()
    saves_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'author', 'description', 'category', 'cook_time', 'difficulty', 'ingredients', 'image', 'likes_count', 'saves_count']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        with transaction.atomic():  # Using atomic transaction to ensure data integrity
            recipe = Recipe.objects.create(**validated_data)
            for ingredient_data in ingredients_data:
                ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)
                recipe.ingredients.add(ingredient)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        
        with transaction.atomic():
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.cook_time = validated_data.get('cook_time', instance.cook_time)
            instance.difficulty = validated_data.get('difficulty', instance.difficulty)
            instance.image = validated_data.get('image', instance.image)
            instance.save()

            # Clear existing ingredients
            instance.ingredients.clear()

            # Add updated ingredients
            for ingredient_data in ingredients_data:
                ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)
                instance.ingredients.add(ingredient)

        return instance
    
    def get_likes_count(self, obj):
        return LikedRecipe.objects.filter(recipe=obj).count()

    def get_saves_count(self, obj):
        return SavedRecipe.objects.filter(recipe=obj).count()