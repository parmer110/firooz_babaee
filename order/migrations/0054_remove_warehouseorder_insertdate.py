# Generated by Django 4.2.1 on 2024-05-11 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0053_alter_warehouseorder_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouseorder',
            name='insertdate',
        ),
    ]
