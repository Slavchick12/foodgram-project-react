from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name='Почта'
    )
    username = models.CharField(
        blank=False,
        max_length=50,
        unique=True,
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        blank=False,
        max_length=50,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        blank=False,
        max_length=50,
        verbose_name='Фамилия'
    )

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
    )

    class Meta:
        ordering = ('user', 'following',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
