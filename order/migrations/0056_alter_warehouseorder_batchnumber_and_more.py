# Generated by Django 4.2.1 on 2024-05-11 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0055_remove_warehouseorder_lastxmldate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouseorder',
            name='batchnumber',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='BN'),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='productionorderid',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='POid'),
        ),
    ]