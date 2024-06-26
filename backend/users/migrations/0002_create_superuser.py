# Generated by Django 2.2.19 on 2024-05-11 13:16

from django.db import migrations
from django.contrib.auth import get_user_model


def create_initial_superuser(apps, schema_editor):
    User = get_user_model()

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@email.com', 'adminadmin')


def revese_migartion():
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_initial_superuser,
            revese_migartion,
        ),
    ]
