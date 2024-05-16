from django.urls import path
from cooks_corner.views import SavedRecipeListView, SavedRecipeCreateView, SavedRecipeDestroyView, LikedRecipeDestroyView, CategoryList, RecipeCreateView, RecipeListView, RecipeDetailView, LikedRecipeListView, SavedRecipeView, LikedRecipeCreateView

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('recipes/', RecipeListView.as_view(), name='recipes-list'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('like-recipes/', LikedRecipeListView.as_view(), name='liked-recipe-list'),
    path('like-recipes/create/', LikedRecipeCreateView.as_view(), name='liked-recipe-create'),
    path('like-recipes/delete/<int:recipe_id>/', LikedRecipeDestroyView.as_view(), name='liked-recipe-delete'),
    path('save-recipes/', SavedRecipeListView.as_view(), name='liked-recipe-list'),
    path('save-recipes/create/', SavedRecipeCreateView.as_view(), name='liked-recipe-create'),
    path('save-recipes/delete/<int:recipe_id>/', LikedRecipeDestroyView.as_view(), name='liked-recipe-delete'),
]