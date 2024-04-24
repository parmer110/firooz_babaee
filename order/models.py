from email.policy import default
from typing import Any
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.deconstruct  import deconstructible
from django.core.validators import MaxLengthValidator, MinLengthValidator
from order.utils.file_utils import unique_file_name
from account.models import CustomUser
from companies.models import Company

class Document(models.Model):

    File_addr = models.FileField(upload_to='XmlFiles/%Y/%m/%d/',verbose_name='انتخاب فایل')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class WarehouseOrder(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    orderid = models.ForeignKey('XMLFile', on_delete=models.CASCADE, related_name="order", verbose_name="شماره سفارش")
    # xml_file = models.ForeignKey('XMLFile', on_delete=models.CASCADE, related_name="order", verbose_name="فایل XML")
    no = models.CharField(verbose_name="تعداد سفارش")
    gtin = models.CharField(max_length=14, blank=True, null=True, verbose_name="کد GTIN")
    batchnumber = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره بچ")
    expdate = models.CharField(max_length=10, blank=True, null=True, verbose_name="تاریخ انقضا")
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, verbose_name="کاربر")
    insertdate = models.CharField(max_length=10, blank=True, null=True, verbose_name="تاریخ درج")
    lastxmldate = models.CharField(max_length=10, blank=True, null=True, verbose_name="آخرین تاریخ XML")
    distributercompanynid = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='warehouse_distributor', verbose_name="کد ملی شرکت توزیع‌کننده")
    ordercompanynid = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='warehouse_order', verbose_name="کد ملی شرکت سفارش دهنده")
    deviceid = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره دستگاه")
    productionorderid = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره سفارش تولید")
    ordertype = models.CharField(max_length=20, blank=True, null=True, verbose_name="نوع سفارش")
    details = models.CharField(max_length=100, blank=True, null=True, verbose_name="جزئیات")
    lc = models.CharField(verbose_name="کد مجوز", null=True, blank=True)
    px = models.CharField(verbose_name="پیش‌شماره مجری")
    wo = models.CharField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'WarehouseOrders'  # تنظیم نام جدول مطابق با SQL Server

    def __str__(self):
        return str(self.orderid)
    

class tblOrder(models.Model):
    STATUS_CHOICES = (
        ('en', 'قابل استعلام'),
        ('dis', 'غیرقابل استعلام'),
    )

    invoicenumber = models.ForeignKey(WarehouseOrder, on_delete=models.CASCADE, verbose_name="شماره سفارش")
    GTIN = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=True, verbose_name="GTIN محصول")
    bn = models.CharField(max_length=14, verbose_name="شماره بچ")
    md = models.CharField(max_length=10, validators=[MinLengthValidator(10)], verbose_name="تاریخ تولید")
    ed = models.CharField(max_length=10, validators=[MinLengthValidator(10)], verbose_name="تاریخ انقضا")
    sc = models.CharField(max_length=20, verbose_name="IRC")
    lc = models.CharField(max_length=20, null=True, verbose_name="کد محلی")
    no = models.PositiveIntegerField(verbose_name="تعداد")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='dis', verbose_name="وضعیت")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.invoicenumber} - {self.status}"


class XMLFile(models.Model):
    STATUS_CHOICES=(
     ('en','قابل استعلام'),
     ('dis','غیرقابل استعلام'),
     )

    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='xmlfiles')
    original_file_name = models.CharField(max_length=255, verbose_name="Original File Name")
    file = models.FileField(upload_to=unique_file_name)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(null=True, blank=True)
    status=models.CharField(STATUS_CHOICES,max_length=3,default='dis')

    def save(self, *args, **kwargs):
        if not self.id:
            self.original_file_name = self.file.name
            super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.original_file_name)
 
    
class Orders (models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    OrderCode = models.ForeignKey(WarehouseOrder, on_delete=models.CASCADE, related_name="order_ordercode")
    SupplierCode = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='order_warehouse_order', verbose_name="کد ملی شرکت سفارش دهنده")
    PublisherCode = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='order_warehouse_distributor', verbose_name="کد ملی شرکت توزیع‌کننده")
    Numberinpack = models.PositiveIntegerField(verbose_name="تعداد")
    BatchNumber = models.CharField(max_length=14, verbose_name="شماره بچ")
    ProduceDate = models.CharField(max_length=10, validators=[MinLengthValidator(10)], verbose_name="تاریخ تولید")
    ExpDate = models.CharField(max_length=10, validators=[MinLengthValidator(10)], verbose_name="تاریخ انقضا")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Orders'

    def __str__(self):
        return str(self.orderid)

