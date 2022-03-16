from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .filters import CustomFilterClass
from .mixins import GETRequestsMixins
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import PageNumberPaginator
from .permissions import AdminUserOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)
from .utils import add_obj, delete_obj


class TagViewSet(GETRequestsMixins):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(GETRequestsMixins):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPaginator
    filter_class = CustomFilterClass
    ordering_fields = ('-pub_date',)
    permission_classes = [AdminUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Recipe.objects.all()
        if self.request.user.is_authenticated:
            user = self.request.user
            if self.request.query_params.get('is_favorited'):
                return queryset.filter(favorites__user=user)
            if self.request.query_params.get('is_in_shopping_cart'):
                return queryset.filter(shopping_cart__user=user)
        return

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return add_obj(request, pk, Recipe, FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return delete_obj(request, pk, Recipe, Favorite)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        return add_obj(request, pk, Recipe, ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return delete_obj(request, pk, Recipe, ShoppingCart)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        queryset = ShoppingCart.objects.filter(user=request.user)
        shoplist = {}
        ingredients = queryset.values_list(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit',
        )
        ingredients_annotated = ingredients.annotate(
            amount_sum=Sum(
                'recipe__recipe_ingredient__amount'
            )
        )
        for ingredient in ingredients_annotated:
            name = ingredient[0]
            measurement_unit = ingredient[1]
            amount = ingredient[2]
            if name not in shoplist:
                shoplist[name] = {
                    'amount': amount,
                    'measurement_unit': measurement_unit
                }
            continue
        content = 'Список покупок:\n'
        for ingredient in shoplist:
            content += (f'{ingredient}'
                        f'({shoplist[ingredient]["measurement_unit"]}) - '
                        f'{shoplist[ingredient]["amount"]}\n')
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment;' 'filename="shoplist.txt"'
        )
        return response
