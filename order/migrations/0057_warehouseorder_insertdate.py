# Generated by Django 4.2.1 on 2024-05-11 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0056_alter_warehouseorder_batchnumber_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouseorder',
            name='insertdate',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
