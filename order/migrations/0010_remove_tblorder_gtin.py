# Generated by Django 4.2.1 on 2024-04-21 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_tblorder_lc_tblorder_sc_alter_tblorder_ed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblorder',
            name='GTIN',
        ),
    ]
