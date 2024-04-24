# Generated by Django 4.2.1 on 2024-04-24 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_warehouseorder_lc_warehouseorder_ordercompanynid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblorder',
            name='invoicenumber',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='order.warehouseorder', verbose_name='شماره سفارش'),
            preserve_default=False,
        ),
    ]
