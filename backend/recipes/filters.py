from django_filters import AllValuesMultipleFilter
from django_filters import rest_framework as filters
from django_filters.widgets import BooleanWidget
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class CustomFilterClass(filters.FilterSet):
    shopping_cart = filters.BooleanFilter(widget=BooleanWidget())
    favorite = filters.BooleanFilter(widget=BooleanWidget())
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    following = AllValuesMultipleFilter(field_name='author__id')

    class Meta:
        model = Recipe
        fields = (
            'author__id',
            'tags__slug',
            'favorite',
            'shopping_cart'
        )


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'
