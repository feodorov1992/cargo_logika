# Generated by Django 4.1.3 on 2023-01-14 15:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0011_order_show_cargo_price_in_receipt'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractorBill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contractor', models.CharField(max_length=255, verbose_name='Contractor name')),
                ('bill_number', models.CharField(max_length=255, verbose_name='Bill number')),
                ('bill_price', models.FloatField(verbose_name='Bill price')),
                ('taxes', models.IntegerField(choices=[(None, 'No taxes'), (20, '20%')], null=True, verbose_name='Taxes')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='logistics.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'contractor bill',
                'verbose_name_plural': 'contractor bills',
                'ordering': ['created_at'],
            },
        ),
    ]
