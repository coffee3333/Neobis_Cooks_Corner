from django.urls import path
from cooks_corner.views.recipes_view import CategoryList, RecipeCreateView, RecipeListView, RecipeDetailView, RecipeImageCreateUpdateDestroyView
from cooks_corner.views.follow_view import FollowListView, FollowCreateView, FollowDestroyView
from cooks_corner.views.like_view import LikedRecipeListView, LikedRecipeCreateView, LikedRecipeDestroyView
from cooks_corner.views.save_view import SavedRecipeListView, SavedRecipeCreateView, SavedRecipeDestroyView


urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    # 
    path('recipes/', RecipeListView.as_view(), name='recipes-list'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/create-image/', RecipeImageCreateUpdateDestroyView.as_view(), name='create-image'),
    #
    path('like-recipes/', LikedRecipeListView.as_view(), name='liked-recipe-list'),
    path('like-recipes/create/', LikedRecipeCreateView.as_view(), name='liked-recipe-create'),
    path('like-recipes/delete/<int:recipe_id>/', LikedRecipeDestroyView.as_view(), name='liked-recipe-delete'),
    # 
    path('save-recipes/', SavedRecipeListView.as_view(), name='liked-recipe-list'),
    path('save-recipes/create/', SavedRecipeCreateView.as_view(), name='liked-recipe-create'),
    path('save-recipes/delete/<int:recipe_id>/', SavedRecipeDestroyView.as_view(), name='liked-recipe-delete'),
    # 
    path('follow-user/', FollowListView.as_view(), name='follow-user-list'),
    path('follow-user/create/', FollowCreateView.as_view(), name='follow-user-create'),
    path('follow-user/delete/<int:followed_id>/', FollowDestroyView.as_view(), name='follow-user-delete'),
]
