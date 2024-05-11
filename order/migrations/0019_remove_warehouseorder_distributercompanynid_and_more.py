# Generated by Django 4.2.1 on 2024-05-01 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0005_rename_nationalid_company_nationalid'),
        ('order', '0018_orders_createdat_orders_updatedat_xmlfile_createdat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouseorder',
            name='distributercompanynid',
        ),
        migrations.RemoveField(
            model_name='warehouseorder',
            name='orderid',
        ),
        migrations.AddField(
            model_name='warehouseorder',
            name='xml_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehouseorder_order', to='order.xmlfile'),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='batchnumber',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='details',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='deviceid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='expdate',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='insertdate',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='lastxmldate',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='lc',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='no',
            field=models.CharField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='ordercompanynid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warehouse_order', to='companies.company'),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='ordertype',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='productionorderid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='px',
            field=models.CharField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='warehouseorder',
            name='userId',
            field=models.ForeignKey(blank=True, db_column='userId', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='warehouseorder',
            name='DistributerCompanyNid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warehouseorder_dc', to='companies.company', verbose_name='dc'),
        ),
        migrations.AddField(
            model_name='warehouseorder',
            name='OrderId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.xmlfile'),
        ),
    ]