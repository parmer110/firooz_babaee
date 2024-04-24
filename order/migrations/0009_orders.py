# Generated by Django 4.2.1 on 2024-04-24 15:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('order', '0008_delete_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('Numberinpack', models.PositiveIntegerField(verbose_name='تعداد')),
                ('BatchNumber', models.CharField(max_length=14, verbose_name='شماره بچ')),
                ('ProduceDate', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)], verbose_name='تاریخ تولید')),
                ('ExpDate', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)], verbose_name='تاریخ انقضا')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('OrderCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_ordercode', to='order.warehouseorder')),
                ('PublisherCode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_warehouse_distributor', to='companies.company', verbose_name='کد ملی شرکت توزیع\u200cکننده')),
                ('SupplierCode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_warehouse_order', to='companies.company', verbose_name='کد ملی شرکت سفارش دهنده')),
            ],
            options={
                'db_table': 'Orders',
            },
        ),
    ]