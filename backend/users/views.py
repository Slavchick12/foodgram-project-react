from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.pagination import PageNumberPaginator

from .models import Follow, User
from .serializers import FollowSerializer, UserSerializer

FOLLOW_YOURSELF_ERROR = 'Нельзя подписываться на себя!'
FOLLOW_USER_ERROR = 'Вы уже подписаны на пользователя!'


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPaginator
    permission_classes = [AllowAny]

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        following = get_object_or_404(User, id=id)
        if user == following:
            return Response({
                'errors': FOLLOW_YOURSELF_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, following=following).exists():
            return Response({
                'errors': FOLLOW_USER_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(user=user, following=following)
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        following = get_object_or_404(User, pk=id)
        subscribe = get_object_or_404(
            Follow,
            user=user,
            following=following
        )
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
