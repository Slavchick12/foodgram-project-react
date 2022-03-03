from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .mixins import GETRequestsMixins
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)
from .pagination import PageNumberPaginator
from .permissions import AdminUserOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)


def add_obj(request, pk, model, model_serializer):
    user = request.user
    recipe = get_object_or_404(model, id=pk)
    data = {
        'user': user.id,
        'recipe': recipe.id,
    }
    serializer = model_serializer(
        data=data,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_obj(request, pk, model, del_model):
    user = request.user
    recipe = get_object_or_404(model, id=pk)
    object = get_object_or_404(
        del_model,
        user=user,
        recipe=recipe
    )
    object.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(GETRequestsMixins):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(GETRequestsMixins):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPaginator
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_fields = ('tags',)
    ordering_fields = ('-pub_date',)
    permission_classes = [AdminUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return add_obj(request, pk, Recipe, FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return delete_obj(request, pk, Recipe, Favorite)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return add_obj(request, pk, Recipe, ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return delete_obj(request, pk, Recipe, ShoppingCart)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, pk=None):
        queryset = ShoppingCart.objects.filter(user=request.user)
        shoplist = {}
        for ingredient in queryset:
            recipe = ingredient.recipe
            ingredients = IngredientInRecipe.objects.filter(recipe=recipe)
            for i in range(len(ingredients)):
                name = ingredients[i].ingredient.name
                measurement_unit = ingredients[i].ingredient.measurement_unit
                if name not in shoplist:
                    A = ingredients.annotate(amount_sum=Sum(
                        'ingredient__ingredient_recipe__amount'
                    ))
                    shoplist[name] = {
                        'amount': A[i].amount_sum,
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
