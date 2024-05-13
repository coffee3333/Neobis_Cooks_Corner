from django.urls import path
from cooks_corner.views import RecipeCreateView, CategoryList, RecipeListView

urlpatterns = [
    path('recipes/new/', RecipeCreateView.as_view(), name='recipe-create'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('recipes/', RecipeListView.as_view(), name='recipes-list'),
]