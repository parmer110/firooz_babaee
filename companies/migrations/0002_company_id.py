# Generated by Django 4.2.1 on 2024-04-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
