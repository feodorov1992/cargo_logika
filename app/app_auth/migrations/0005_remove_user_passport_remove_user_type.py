# Generated by Django 4.1.3 on 2023-01-07 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0004_user_contract'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='passport',
        ),
        migrations.RemoveField(
            model_name='user',
            name='type',
        ),
    ]