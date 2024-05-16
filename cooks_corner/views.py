from drf_yasg import openapi
from rest_framework import mixins, generics, status, permissions
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from authentication.permissions import IsOwnerOrReadOnly
from cooks_corner.models import Recipe, Category, LikedRecipe, SavedRecipe
from cooks_corner.pagination import CustomPagination
from cooks_corner.serializers import SavedRecipeListSerializer, SavedRecipeSerializer, RecipeSerializer, CategorySerializer, RecipeListSerializer, LikedRecipeSerializer, SavedRecipeSerializer, LikedRecipeListSerializer
from cooks_corner.filters import RecipeFilter
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404

import logging
logger = logging.getLogger(__name__)


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]


class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all().order_by('id') 
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeCreateView(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            # Set the recipe author to the current user upon creation
            serializer.save(author=self.request.user)
        except Exception as e:
            # Log the exception
            logger.error(f'Error occurred while creating the recipe: {e}')
            raise e  # Re-raise the exception for Django to handle


class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Разрешение на чтение для всех, редактирование и удаление для аутентифицированных пользователей

    def perform_update(self, serializer):
        # Можно добавить дополнительные действия при обновлении, если необходимо
        serializer.save()

    def perform_destroy(self, instance):
        # Можно добавить дополнительные действия перед удалением, если необходимо
        instance.delete()


class LikedRecipeListView(generics.ListAPIView):
    queryset = LikedRecipe.objects.all()
    serializer_class = LikedRecipeListSerializer
    permission_classes = [permissions.IsAuthenticated]


class LikedRecipeCreateView(generics.CreateAPIView):
    queryset = LikedRecipe.objects.all()
    serializer_class = LikedRecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError({"error": "You have already liked this recipe."})


class LikedRecipeDestroyView(generics.DestroyAPIView):
    queryset = LikedRecipe.objects.all()
    serializer_class = LikedRecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        user = request.user
        recipe_id = kwargs.get('recipe_id')

        try:
            liked_recipe = get_object_or_404(LikedRecipe, user=user, recipe_id=recipe_id)
            liked_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LikedRecipe.DoesNotExist:
            return Response({"error": "Liked recipe not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SavedRecipeView(generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SavedRecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            return Response({"error": "You have already saved this recipe."}, status=status.HTTP_400_BAD_REQUEST)
        
class SavedRecipeListView(generics.ListAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SavedRecipeListSerializer
    permission_classes = [permissions.IsAuthenticated]


class SavedRecipeCreateView(generics.CreateAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SavedRecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError({"error": "You have already liked this recipe."})


class SavedRecipeDestroyView(generics.DestroyAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SavedRecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        user = request.user
        recipe_id = kwargs.get('recipe_id')

        try:
            liked_recipe = get_object_or_404(LikedRecipe, user=user, recipe_id=recipe_id)
            liked_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LikedRecipe.DoesNotExist:
            return Response({"error": "Liked recipe not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)