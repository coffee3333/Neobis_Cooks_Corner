import django_filters
from cooks_corner.models import Recipe

class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author_username = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    author_id = django_filters.NumberFilter(field_name='author__id')
    category_id = django_filters.NumberFilter(field_name='category__id')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Recipe
        fields = ['author_id', 'author_username', 'category_id', 'category_name']
