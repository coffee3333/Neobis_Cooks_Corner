from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from cooks_corner.models import LikedRecipe
from cooks_corner.serializers import LikedRecipeListSerializer, LikedRecipeSerializer
from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authentication.permissions import IsOwnerOrReadOnly


class LikedRecipeListView(generics.ListAPIView):
    queryset = LikedRecipe.objects.all()
    serializer_class = LikedRecipeListSerializer
    permission_classes = [IsAuthenticated]


class LikedRecipeCreateView(generics.CreateAPIView):
    queryset = LikedRecipe.objects.all()
    serializer_class = LikedRecipeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError({"error": "You have already liked this recipe."})


class LikedRecipeDestroyView(generics.DestroyAPIView):
    queryset = LikedRecipe.objects.all()
    serializer_class = LikedRecipeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

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