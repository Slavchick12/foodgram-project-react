# Generated by Django 2.2.19 on 2022-03-20 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220318_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=50, verbose_name='единица измерения'),
        ),
    ]