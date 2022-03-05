from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User


FOLLOW_YOURSELF_ERROR = 'Невозможно подписаться на себя!'
REPEATED_FOLLOW_ERROR = 'Вы уже подписаны на данного автора!'


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Follow.objects.filter(
            user=request.user,
            following=obj.id
        ).exists()

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class FollowSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    following = serializers.PrimaryKeyRelatedField(queryset=queryset)
    validators = [
        UniqueTogetherValidator(
            queryset=Follow.objects.all(), fields=('following', 'user')
        )
    ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise ValidationError(FOLLOW_YOURSELF_ERROR)
        if Follow.objects.filter(
            user=data['user'],
            following=data['following']
        ).exists():
            raise ValidationError(REPEATED_FOLLOW_ERROR)
        return data

    class Meta:
        model = Follow
        fields = (
            'user',
            'following'
        )
