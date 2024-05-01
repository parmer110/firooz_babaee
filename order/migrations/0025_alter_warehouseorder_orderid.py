# Generated by Django 4.2.1 on 2024-05-01 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0024_warehouseorder_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouseorder',
            name='OrderId',
            field=models.ForeignKey(db_column='OrderId', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='order', serialize=False, to='order.xmlfile', unique=True),
        ),
    ]
