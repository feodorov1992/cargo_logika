# Generated by Django 4.1.3 on 2023-01-06 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0002_user_is_customer_user_org_name_user_passport_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_customer',
        ),
    ]
