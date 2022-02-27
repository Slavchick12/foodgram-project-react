from colorfield.fields import ColorField
from django.db import models

from users.models import User

UNITS = [
    ('мг', 'мг'),
    ('г', 'г'),
    ('кг', 'кг')
]


class Tag(models.Model):
    name = models.CharField(
        'название',
        unique=True,
        max_length=50,
        help_text='Название тега'
    )
    slug = models.SlugField(max_length=50)
    color = ColorField()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'название',
        max_length=50,
        help_text='Название ингридиента'
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=50,
        choices=UNITS,
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество',
        help_text='Количество ингредиента',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'название',
        max_length=50,
        help_text='Название рецепта'
    )
    text = models.TextField('текст', help_text='Здесь Ваш текст')
    pub_date = models.DateTimeField(
        'дата публикации', auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True, null=True,
        help_text='Можете загрузить картинку',
        verbose_name='картинка',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tag',
        verbose_name='тег',
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        help_text='Время приготовления в минутах',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredient',
        verbose_name='ингридиент',
    )
    description = models.TextField('описание', help_text='Описание')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='автор'
    )

    class Meta:
        ordering = ('recipe', 'user')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user}, {self.recipe}'
