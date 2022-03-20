from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import IngredientInRecipe


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


def get_is_obj(self, obj, model):
    request = self.context.get('request')
    if request.user.is_anonymous:
        return False
    return model.objects.filter(
        user=request.user,
        recipe=obj
    ).exists()


def add_ingredients(instance, **validated_data):
    ingredients = validated_data['ingredients']
    print(ingredients)
    for ingredient in ingredients:
        IngredientInRecipe.objects.create(
            recipe=instance,
            ingredient_id=ingredient.get('id'),
            amount=ingredient['amount']
        )
    return instance
