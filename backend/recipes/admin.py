from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Recipe, ShoppingCart, Tag


class IngredientInRecipetInLine(admin.TabularInline):
    model = IngredientInRecipe
    fk_name = 'recipe'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'text',
        'pub_date',
        'author',
        'image',
        'cooking_time',
        'description'
    )
    search_fields = ('name', 'author', 'tags')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    inlines = [IngredientInRecipetInLine]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
