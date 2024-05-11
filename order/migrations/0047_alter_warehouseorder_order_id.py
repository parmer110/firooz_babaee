# Generated by Django 4.2.1 on 2024-05-09 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0046_warehouseorder_order_id_alter_warehouseorder_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouseorder',
            name='order_id',
            field=models.ForeignKey(db_column='OrderId', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='order.xmlfile'),
        ),
    ]