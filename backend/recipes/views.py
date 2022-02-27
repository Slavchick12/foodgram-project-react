from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import PageNumberPaginator
from .permissions import AuthorOrAdminOrRead
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)


class GETRequestsMixins(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [AllowAny]


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
    permission_classes = [AuthorOrAdminOrRead]

    def perfome_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': user.id,
            'recipe': recipe.id,
        }
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(
            Favorite,
            user=user,
            recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': user.id,
            'recipe': recipe.id,
        }
        serializer = ShoppingCartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart_recipe = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
        )
        shopping_cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, pk=None):
        queryset = ShoppingCart.objects.filter(user=request.user).all()
        print(queryset)
        ingredients = queryset.values_list(
            'recipe__ingredients__ingredient__name',
            'recipe__ingredients__measurement_unit',
            'recipe__ingredients__amount'
        )
        text = 'Список покупок: \n'
        shoplist = {}
        for ingredient in ingredients:
            name, measurement_unit, amount = ingredient
            if name not in shoplist:
                shoplist[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                shoplist[name]['amount'] += amount
        text += f'{str(shoplist)}'
        response = HttpResponse(text, 'Content-Type: text/plane')
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
        return response
