# Generated by Django 4.2.1 on 2024-05-14 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_producercompanycode'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
