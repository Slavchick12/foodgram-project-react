import json

from django.db import migrations


def create_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')

    with open('fixtures/ingredients.json', 'r', encoding='utf-8') as intgrediets_file:
        ingrediet_objects = []
        ingrediets = json.load(intgrediets_file)

        for ingrediet in ingrediets:
            ingrediet_objects.append(
                Ingredient(
                    name=ingrediet['name'],
                    measurement_unit=ingrediet['measurement_unit'],
                )
            )

        Ingredient.objects.bulk_create(ingrediet_objects)


def backwards(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    Ingredient.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0004_auto_20240511_1549'),
    ]

    operations = [
        migrations.RunPython(create_ingredients, backwards),
    ]
