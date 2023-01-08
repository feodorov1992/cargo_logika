# Generated by Django 4.1.3 on 2023-01-07 19:36

from django.db import migrations, models
import django.db.models.deletion
import log_cats.models


class Migration(migrations.Migration):

    dependencies = [
        ('log_cats', '0001_initial'),
        ('logistics', '0009_alter_order_payer_tin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_type',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_type',
            field=models.ForeignKey(default=log_cats.models.DeliveryType.get_default_pk, on_delete=django.db.models.deletion.PROTECT, to='log_cats.deliverytype', verbose_name='Type of delivery'),
        ),
    ]