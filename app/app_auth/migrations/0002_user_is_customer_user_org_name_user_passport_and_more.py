# Generated by Django 4.1.3 on 2023-01-06 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=True, verbose_name='Is a customer'),
        ),
        migrations.AddField(
            model_name='user',
            name='org_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Organisation name'),
        ),
        migrations.AddField(
            model_name='user',
            name='passport',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Payer passport'),
        ),
        migrations.AddField(
            model_name='user',
            name='tin',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='User TIN'),
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('individual', 'Individual'), ('company', 'Company')], default='individual', max_length=15, verbose_name='User type'),
        ),
    ]
