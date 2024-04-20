# Generated by Django 4.2.1 on 2024-04-20 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import order.utils.file_utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0003_rename_user_tblxmlorders_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblxmlorders',
            name='error_message',
        ),
        migrations.RemoveField(
            model_name='tblxmlorders',
            name='file',
        ),
        migrations.RemoveField(
            model_name='tblxmlorders',
            name='original_file_name',
        ),
        migrations.CreateModel(
            name='XMLFile',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('original_file_name', models.CharField(max_length=255, verbose_name='Original File Name')),
                ('file', models.FileField(upload_to=order.utils.file_utils.unique_file_name)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xmlfiles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
