from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


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
