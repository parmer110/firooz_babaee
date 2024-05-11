# Generated by Django 4.2.1 on 2024-05-01 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcode', '0007_alter_barcode_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barcode',
            name='favoritecode',
        ),
        migrations.RemoveField(
            model_name='barcode',
            name='orderserial',
        ),
        migrations.AlterField(
            model_name='barcode',
            name='UUIDCount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]