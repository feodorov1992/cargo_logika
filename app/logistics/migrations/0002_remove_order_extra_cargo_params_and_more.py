# Generated by Django 4.1.3 on 2022-12-19 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='extra_cargo_params',
        ),
        migrations.DeleteModel(
            name='ExtraCargoParam',
        ),
    ]
