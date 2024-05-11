# Generated by Django 4.2.1 on 2024-05-01 14:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_id'),
        ('companies', '0002_company_id'),
        ('order', '0016_remove_orders_publishercode_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='Numberinpack',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='OrderCode',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='createdAt',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='updatedAt',
        ),
        migrations.RemoveField(
            model_name='xmlfile',
            name='dc',
        ),
        migrations.RemoveField(
            model_name='xmlfile',
            name='no',
        ),
        migrations.RemoveField(
            model_name='xmlfile',
            name='oc',
        ),
        migrations.RemoveField(
            model_name='xmlfile',
            name='ot',
        ),
        migrations.AddField(
            model_name='orders',
            name='NumberOfOrder',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='ProductCode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='gtin'),
        ),
        migrations.AddField(
            model_name='orders',
            name='xmlfile_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='odd', to='order.xmlfile'),
        ),
        migrations.AddField(
            model_name='xmlfile',
            name='NumberOfOrder',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='xmlfile',
            name='OrderCode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_warehouse_distributor', to='companies.company', verbose_name='dc'),
        ),
        migrations.AddField(
            model_name='xmlfile',
            name='OrderType',
            field=models.CharField(choices=[('inc', 'incomming'), ('out', 'outgoing'), ('rtn', 'returning')], default='', max_length=3, verbose_name='ot'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='xmlfile',
            name='SupplierCode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_warehouse_order', to='companies.company', verbose_name='oc'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='BatchNumber',
            field=models.CharField(max_length=14, verbose_name='bn'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='ExpDate',
            field=models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)], verbose_name='ed'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='ProduceDate',
            field=models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)], verbose_name='md'),
        ),
    ]