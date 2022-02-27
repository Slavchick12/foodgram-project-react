from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )

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
            raise ValidationError('Невозможно подписаться на себя!')
        if Follow.objects.filter(
            user=data['user'],
            following=data['following']
        ).exists():
            raise ValidationError('Вы уже подписаны на данного автора!')
        return data

    class Meta:
        model = Follow
        fields = (
            'user',
            'following'
        )
