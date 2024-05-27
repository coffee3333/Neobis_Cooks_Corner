from drf_yasg import openapi
from rest_framework import  generics, status, permissions
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from authentication.permissions import IsOwnerOrReadOnly
from cooks_corner.models import Recipe, Category, RecipeImage
from cooks_corner.pagination import CustomPagination
from cooks_corner.filters import RecipeFilter
from cooks_corner.serializers import (
    RecipeSerializer, 
    CategorySerializer, 
    RecipeListSerializer, 
    RecipeImageSerializer,
)


class CategoryList(generics.ListCreateAPIView):
    """
    Category of the recipes.

    Category of the recipes. This endpoint provides creating Category and list of Categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]


class RecipeListView(generics.ListAPIView):
    """
    List of the recipes.

    List of the recipes. This endpoint provides to get list of recipes with following fillters.
    """
    queryset = Recipe.objects.all().order_by('id') 
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="Title", type=openapi.TYPE_STRING),
        openapi.Parameter('author_username', openapi.IN_QUERY, description="Author Username", type=openapi.TYPE_STRING),
        openapi.Parameter('author_id', openapi.IN_QUERY, description="Author ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('category_id', openapi.IN_QUERY, description="Category ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('category_name', openapi.IN_QUERY, description="Category Name", type=openapi.TYPE_STRING),
        openapi.Parameter('saved_by_user', openapi.IN_QUERY, description="Saved by User", type=openapi.TYPE_BOOLEAN),
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('limit', openapi.IN_QUERY, description="Number of results to return per page", type=openapi.TYPE_INTEGER),
    ])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_filterset(self, *args, **kwargs):
        kwargs['request'] = self.request
        return super().get_filterset(*args, **kwargs)


class RecipeCreateView(generics.CreateAPIView):
    """
    Create of the recipe.

    Create of the recipe. This endpoint provides to create recipe with ingredients.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except Exception as e:
            return Response({"error": f'Error occurred while creating the recipe: {e}'}, status=status.HTTP_404_NOT_FOUND)


class RecipeDetailView(generics.RetrieveAPIView):
    """
    Detail of the recipe.

    Detail of the recipe. This endpoint provides to Detail of the recipe.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Разрешение на чтение для всех, редактирование и удаление для аутентифицированных пользователей

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class RecipeImageCreateUpdateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):
    """
    Create and delete the recipes images.

    Create and delete the recipes images. This endpoint provides to create and delete the images of the recipes.
    """
    queryset = RecipeImage.objects.all()
    serializer_class = RecipeImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]