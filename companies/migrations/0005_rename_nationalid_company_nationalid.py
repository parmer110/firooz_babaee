# Generated by Django 4.2.1 on 2024-05-01 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_alter_company_nationalid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='nationalid',
            new_name='NationalId',
        ),
    ]