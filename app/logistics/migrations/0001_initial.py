# Generated by Django 4.1.3 on 2022-12-11 00:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import logistics.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
            ],
            options={
                'verbose_name': 'delivery type',
                'verbose_name_plural': 'delivery types',
            },
        ),
        migrations.CreateModel(
            name='ExtraCargoParam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
            ],
            options={
                'verbose_name': 'extra cargo parameter',
                'verbose_name_plural': 'extra cargo parameters',
            },
        ),
        migrations.CreateModel(
            name='ExtraService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
            ],
            options={
                'verbose_name': 'extra service',
                'verbose_name_plural': 'extra services',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_number', models.CharField(default=logistics.models.default_order_num, max_length=7, verbose_name='Order number')),
                ('order_date', models.DateField(default=django.utils.timezone.now, verbose_name='Order date')),
                ('payer_name', models.CharField(max_length=255, verbose_name='Payer')),
                ('payer_type', models.CharField(choices=[('individual', 'Individual'), ('company', 'Company')], default='individual', max_length=15, verbose_name='Payer type')),
                ('payment_type', models.CharField(choices=[('cash', 'Cash payment'), ('cashless', 'Cashless payment')], default='cash', max_length=15, verbose_name='Payment type')),
                ('payer_passport', models.CharField(blank=True, max_length=30, null=True, verbose_name='Payer passport')),
                ('payer_tin', models.CharField(blank=True, max_length=15, null=True, verbose_name='Payer TIN')),
                ('payer_email', models.EmailField(max_length=254, verbose_name='Payer email')),
                ('payer_phone', models.CharField(max_length=50, verbose_name='Payer phone')),
                ('payer_contact', models.CharField(max_length=100, verbose_name='Payer contact')),
                ('cargo_name', models.CharField(max_length=255, verbose_name='Cargo name')),
                ('package_type', models.CharField(choices=[('pallet', 'Pallet'), ('bulk', 'Bulk')], default='pallet', max_length=15, verbose_name='Package type')),
                ('cargo_spaces', models.IntegerField(blank=True, null=True, verbose_name='Cargo spaces')),
                ('cargo_weight', models.FloatField(blank=True, null=True, verbose_name='Cargo weight, kg')),
                ('cargo_volume', models.FloatField(blank=True, null=True, verbose_name='Cargo volume, m3')),
                ('insurance', models.BooleanField(default=False, verbose_name='Insurance is required')),
                ('cargo_value', models.FloatField(blank=True, null=True, verbose_name='Cargo value')),
                ('sender_name', models.CharField(max_length=255, verbose_name='Sender')),
                ('sender_type', models.CharField(choices=[('individual', 'Individual'), ('company', 'Company')], default='individual', max_length=15, verbose_name='Sender type')),
                ('sender_passport', models.CharField(blank=True, max_length=30, null=True, verbose_name='Sender passport')),
                ('sender_tin', models.CharField(blank=True, max_length=15, null=True, verbose_name='Sender TIN')),
                ('sender_phone', models.CharField(max_length=50, verbose_name='Sender phone')),
                ('sender_contact', models.CharField(max_length=100, verbose_name='Sender contact')),
                ('sender_addr', models.CharField(max_length=255, verbose_name='Departure city')),
                ('send_precise_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Departure address')),
                ('loading_by', models.CharField(choices=[('cargo_logika', 'Loading by "CARGO LOGIKA"'), ('sender', 'Loading by sender')], default='cargo_logika', max_length=30, verbose_name='Loading by')),
                ('receiver_name', models.CharField(max_length=255, verbose_name='Receiver')),
                ('receiver_type', models.CharField(choices=[('individual', 'Individual'), ('company', 'Company')], default='individual', max_length=15, verbose_name='Receiver type')),
                ('receiver_passport', models.CharField(blank=True, max_length=30, null=True, verbose_name='Receiver passport')),
                ('receiver_tin', models.CharField(blank=True, max_length=15, null=True, verbose_name='Receiver TIN')),
                ('receiver_phone', models.CharField(max_length=50, verbose_name='Receiver phone')),
                ('receiver_contact', models.CharField(max_length=100, verbose_name='Receiver contact')),
                ('receiver_addr', models.CharField(max_length=255, verbose_name='Delivery city')),
                ('receiver_precise_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Full delivery address')),
                ('unloading_by', models.CharField(choices=[('cargo_logika', 'Unloading by "CARGO LOGIKA"'), ('receiver', 'Unloading by receiver')], default='cargo_logika', max_length=30, verbose_name='Unloading by')),
                ('extra_info', models.TextField(blank=True, null=True, verbose_name='Extra info')),
                ('pickup_date', models.DateField(blank=True, null=True, verbose_name='Date of pickup')),
                ('picked_up', models.BooleanField(default=False, verbose_name='Cargo picked up')),
                ('delivery_date', models.DateField(blank=True, null=True, verbose_name='Date of delivery')),
                ('delivered', models.BooleanField(default=False, verbose_name='Cargo delivered')),
                ('docs_sent', models.CharField(choices=[('no', 'No'), ('yes', 'Yes'), ('edm', 'EDM')], default='no', max_length=5, verbose_name='Docs sent')),
                ('contractor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Contractor')),
                ('contractor_waybill', models.CharField(blank=True, max_length=50, null=True, verbose_name='Contractor waybill')),
                ('expenses', models.FloatField(blank=True, null=True, verbose_name='Transit expenses, rub')),
                ('order_price', models.FloatField(blank=True, null=True, verbose_name='Transit price, rub')),
                ('insurance_price', models.FloatField(blank=True, null=True, verbose_name='Insurance price, rub')),
                ('insurance_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Insurance bill number')),
                ('bill_date', models.DateField(blank=True, null=True, verbose_name='Date of bill')),
                ('bill_sent', models.BooleanField(default=False, verbose_name='Bill sent')),
                ('bill_payed', models.BooleanField(default=False, verbose_name='Bill payed')),
                ('load_unload', models.BooleanField(default=True, verbose_name='Loading/unloading required')),
                ('hidden_status', models.CharField(blank=True, max_length=255, null=True, verbose_name='Hidden status')),
                ('contract', models.CharField(blank=True, max_length=255, null=True, verbose_name='Contract number')),
                ('accounts_email_sent', models.BooleanField(default=False, verbose_name='Email to the accounts manager sent')),
                ('delivery_type', models.ManyToManyField(blank=True, to='logistics.deliverytype', verbose_name='Type of delivery')),
                ('extra_cargo_params', models.ManyToManyField(blank=True, to='logistics.extracargoparam', verbose_name='Extra cargo parameters')),
                ('extra_services', models.ManyToManyField(blank=True, to='logistics.extraservice', verbose_name='Extra services')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ['-order_number'],
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=255, verbose_name='Status label')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Date of status change')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='logistics.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'order status',
                'verbose_name_plural': 'order statuses',
                'ordering': ['date'],
            },
        ),
    ]