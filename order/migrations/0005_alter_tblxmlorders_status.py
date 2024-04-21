# Generated by Django 4.2.1 on 2024-04-21 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_remove_tblxmlorders_error_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblxmlorders',
            name='status',
            field=models.CharField(choices=[('en', 'قابل استعلام'), ('dis', 'غیرقابل استعلام')], default='dis', max_length=3),
        ),
    ]
