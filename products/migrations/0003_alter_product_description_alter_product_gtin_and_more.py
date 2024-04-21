# Generated by Django 4.2.1 on 2024-04-21 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='product',
            name='gtin',
            field=models.CharField(max_length=13, primary_key=True, serialize=False, verbose_name='کد جهانی تجاری'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='عکس'),
        ),
    ]
