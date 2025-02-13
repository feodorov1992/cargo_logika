# Generated by Django 4.1.10 on 2023-08-16 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50, verbose_name='label')),
                ('file', models.FileField(upload_to='docs/', verbose_name='file')),
            ],
            options={
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
        ),
        migrations.CreateModel(
            name='IconBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering_num', models.IntegerField(default=0, verbose_name='ordering_num')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('text', models.CharField(max_length=255, verbose_name='text')),
                ('img', models.ImageField(upload_to='main_icons/', verbose_name='icon')),
            ],
            options={
                'verbose_name': 'icon block',
                'verbose_name_plural': 'icon blocks',
                'ordering': ['ordering_num', 'id'],
            },
        ),
        migrations.CreateModel(
            name='MetaTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'meta tag',
                'verbose_name_plural': 'meta tags',
            },
        ),
        migrations.CreateModel(
            name='PhotoBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering_num', models.IntegerField(default=0, verbose_name='ordering_num')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('text', models.TextField(verbose_name='text')),
                ('img', models.ImageField(upload_to='main_photos/', verbose_name='photo')),
            ],
            options={
                'verbose_name': 'photo block',
                'verbose_name_plural': 'photo blocks',
                'ordering': ['ordering_num', 'id'],
            },
        ),
    ]
