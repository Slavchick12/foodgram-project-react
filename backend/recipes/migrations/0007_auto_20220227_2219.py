# Generated by Django 2.2.19 on 2022-02-27 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20220227_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='amount',
            field=models.PositiveSmallIntegerField(default=1, help_text='Количество ингредиента'),
        ),
        migrations.DeleteModel(
            name='IngredientsInRecipe',
        ),
    ]
