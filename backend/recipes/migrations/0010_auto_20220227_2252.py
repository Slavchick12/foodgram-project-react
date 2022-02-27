# Generated by Django 2.2.19 on 2022-02-27 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20220227_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='amount',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(default=1, help_text='Количество ингредиента', verbose_name='Количество'),
        ),
    ]
