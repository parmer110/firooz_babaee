# Generated by Django 4.2.1 on 2024-05-01 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcode', '0002_alter_barcode_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='barcode',
            name='orderid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]