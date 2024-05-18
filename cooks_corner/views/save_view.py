from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from cooks_corner.models import SavedRecipe
from cooks_corner.serializers import SavedRecipeListSerializer, SavedRecipeSerializer
from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authentication.permissions import IsOwnerOrReadOnly


class SavedRecipeListView(generics.ListAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SavedRecipeListSerializer
    permission_classes = [IsAuthenticated]


class SavedRecipeCreateView(generics.CreateAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SavedRecipeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError({"error": "You have already saved this recipe."})


class SavedRecipeDestroyView(generics.DestroyAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SavedRecipeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        user = request.user
        recipe_id = kwargs.get('recipe_id')

        try:
            liked_recipe = get_object_or_404(SavedRecipe, user=user, recipe_id=recipe_id)
            liked_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SavedRecipe.DoesNotExist:
            return Response({"error": "Saved recipe not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)