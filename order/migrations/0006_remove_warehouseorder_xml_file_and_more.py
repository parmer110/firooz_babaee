# Generated by Django 4.2.1 on 2024-04-24 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_tblorder_invoicenumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouseorder',
            name='xml_file',
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='orderid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.xmlfile', verbose_name='شماره سفارش'),
        ),
    ]