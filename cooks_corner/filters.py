import django_filters
from cooks_corner.models import Recipe
from authentication.models import User

class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author_username = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    author_id = django_filters.NumberFilter(field_name='author__id')
    category_id = django_filters.NumberFilter(field_name='category__id')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    saved_by_user = django_filters.BooleanFilter(method='filter_saved_by_user')

    class Meta:
        model = Recipe
        fields = ['author_id', 'author_username', 'category_id', 'category_name', 'saved_by_user']

    def filter_saved_by_user(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(saved_by__user=user)
        return queryset


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username']