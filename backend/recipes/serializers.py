from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User
from users.serializers import UserSerializer

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)
from .utils import get_is_obj

COOKING_TIME_MORE_ZERO = 'Время готовки должно быть больше нуля!'
FAVORITE_ADDED = 'Рецепт уже добавлен в избранное!'
INGREDIENT_ADDED = 'Ингредиент не должен повторяться!'
TAG_ADDED = 'Тег не должен повторяться!'
SHOPLIST_ADDED = 'Рецепт уже добавлен в список покупок!'
INGREDIENT_MORE_ZERO = 'Количество ингредиента должно быть больше 0!'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'slug',
            'color'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True,)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_in_shopping_cart(self, obj):
        return get_is_obj(self, obj, ShoppingCart)

    def get_is_favorited(self, obj):
        return get_is_obj(self, obj, Favorite)


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientInRecipeSerializer(many=True,)
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'name',
            'image',
            'ingredients',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        print(data)
        ingredients = data['ingredients']
        tags = data['tags']
        data_list = []
        for ingredient in ingredients:
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(INGREDIENT_MORE_ZERO)
            if ingredient in data_list:
                raise serializers.ValidationError(INGREDIENT_ADDED)
            else:
                data_list.append(ingredient)
        for tag in tags:
            if tag in data_list:
                raise serializers.ValidationError(TAG_ADDED)
            else:
                data_list.append(tag)
        if data['cooking_time'] <= 0:
            raise serializers.ValidationError(COOKING_TIME_MORE_ZERO)
        del data_list
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def add_ingredients(self, instance, **validated_data):
        ingredients = validated_data['ingredients']
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                recipe=instance,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount']
            )
        return instance

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        return self.add_ingredients(
            recipe,
            ingredients=ingredients,
        )

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        instance = self.add_ingredients(
            instance,
            ingredients=ingredients,
        )
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            'id',
            'recipe',
            'user'
        )

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if Favorite.objects.filter(user=user, recipe__id=recipe_id).exists():
            raise ValidationError(FAVORITE_ADDED)
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'recipe',
            'user'
        )

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if ShoppingCart.objects.filter(
            user=user,
            recipe__id=recipe_id
        ).exists():
            raise ValidationError(SHOPLIST_ADDED)
        return data
