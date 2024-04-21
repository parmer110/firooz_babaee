# Generated by Django 4.2.1 on 2024-04-21 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_description_alter_product_gtin_and_more'),
        ('order', '0010_remove_tblorder_gtin'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblorder',
            name='GTIN',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]
