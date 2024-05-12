from email.policy import default
from typing import Any
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.deconstruct  import deconstructible
from django.core.validators import MaxLengthValidator, MinLengthValidator
from order.utils.file_utils import unique_file_name
from django.db.models.signals import pre_save
from django.dispatch import receiver
from account.models import CustomUser
from companies.models import Company

class Document(models.Model):

    File_addr = models.FileField(upload_to='XmlFiles/%Y/%m/%d/',verbose_name='انتخاب فایل')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class tblOrder(models.Model):
    STATUS_CHOICES = (
        ('en', 'قابل استعلام'),
        ('dis', 'غیرقابل استعلام'),
    )

    invoicenumber = models.ForeignKey('WarehouseOrder', on_delete=models.CASCADE, verbose_name="شماره سفارش")
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
        try:
            return f"{self.invoicenumber} - {self.status}"
        except self._meta.model.DoesNotExist:
            return "Undefined"

class Level(models.Model):
    id = models.AutoField(primary_key=True)  # از نوع AutoField برای identity استفاده شده
    levelId = models.IntegerField(unique=True, verbose_name="شناسه سطح")
    level_name = models.CharField(max_length=128, blank=True, null=True, verbose_name="نام سطح")
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="کاربر")
    insert_date = models.DateField(auto_now_add=True, verbose_name="تاریخ درج")

    class Meta:
        db_table = 'Levels'
        verbose_name = 'سطح'
        verbose_name_plural = 'سطوح'

    def __str__(self):
        return f"{self.level_name} ({self.levelId})"

class WareHouseOrderLevels(models.Model):
    order = models.ForeignKey(
        'WarehouseOrder',
        on_delete=models.CASCADE,
        related_name='levels',
        verbose_name="سفارش",
        db_index=True
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        verbose_name="سطح",
        db_index=True
    )
    number_of_order = models.IntegerField(
        verbose_name="تعداد سفارش",
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'warehouse_order_levels'
        verbose_name = 'سطح سفارش انبار'
        verbose_name_plural = 'سطوح سفارشات انبار'

    def __str__(self):
        return f"{self.order.id} - {self.level.id} - {self.number_of_order}"


class XMLFile(models.Model):
    STATUS_CHOICES=(
     ('en','قابل استعلام'),
     ('dis','غیرقابل استعلام'),
    )
    ORDER_TYPE=(
        ('incomming', 'incomming'),
        ('outgoing', 'outgoing'),
        ('returning', 'returning')
    )

    id = models.AutoField(primary_key=True, editable=False)
    NumberOfOrder = models.PositiveIntegerField(null=True, blank=True, verbose_name="NO")
    SupplierCode = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, 
                                related_name='xmlfile_oc', verbose_name="oc", db_column="supplier_code")
    PublisherCode = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, 
                                related_name='order_warehouse_distributor', verbose_name="dc", db_column="publisher_code")
    OrderType = models.CharField(max_length=10, choices=ORDER_TYPE, verbose_name="ot", default="outgoing")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='xmlfiles', db_column="user")
    original_file_name = models.CharField(max_length=255, verbose_name="Original File Name")
    file = models.FileField(upload_to=unique_file_name)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    error_message = models.TextField(null=True, blank=True)
    status=models.CharField(STATUS_CHOICES,max_length=3,default='dis')

    class Meta:
        db_table = "XMLFiles"

    def save(self, *args, **kwargs):
        if not self.id:
            self.original_file_name = self.file.name
            super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id)
 
    
class Orders (models.Model):
    OrderCode = models.AutoField(primary_key=True, editable=False)
    xmlfile_id = models.ForeignKey(XMLFile, on_delete=models.CASCADE, related_name="odd", null=True)
    NumberOfOrder = models.PositiveIntegerField(null=True, blank=True, verbose_name='no')
    BatchNumber = models.CharField(max_length=14, verbose_name="bn")
    ProduceDate = models.CharField(max_length=10, validators=[MinLengthValidator(10)], verbose_name="md")
    ExpDate = models.CharField(max_length=10, validators=[MinLengthValidator(10)], verbose_name="ed")
    ProductCode = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=True, verbose_name="gtin")
    LicenceCode = models.CharField(max_length=20, verbose_name="lc", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Orders'

    def __str__(self):
        return str(self.OrderCode)


class WarehouseOrder(models.Model):
    ORDER_TYPE=(
        ('incomming', 'incomming'),
        ('outgoing', 'outgoing'),
        ('returning', 'returning')
    )
    id = models.PositiveIntegerField(unique=True, editable=False)
    OrderId = models.PositiveIntegerField(db_column='OrderId', primary_key=True)
    DistributerCompanyNid = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, 
        related_name='DC', verbose_name="dc", db_column="DistributerCompanyNid")
    ordertype = models.CharField(max_length=10, choices=ORDER_TYPE, verbose_name="ot")
    no = models.CharField(null=True, blank=True, default="")
    gtin = models.CharField(max_length=14, blank=True, null=True, verbose_name="کد GTIN")
    batchnumber = models.CharField(max_length=20, blank=True, null=True, verbose_name="BN")
    expdate = models.CharField(max_length=10, blank=True, null=True)
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, db_column='userId')
    insertdate = models.CharField(max_length=10, blank=True, null=True)
    lastxmldate = models.CharField(max_length=10, blank=True, null=True)
    ordercompanynid = models.ForeignKey(Company, on_delete=models.SET_NULL, db_column="ordercompanynid",
        null=True, blank=True, related_name='warehouse_order', verbose_name='OC')
    DeviceId = models.CharField(max_length=20, blank=True, null=True)
    productionorderid = models.CharField(max_length=20, blank=True, null=True, verbose_name="POid")
    details = models.CharField(max_length=100, blank=True, null=True)
    lc = models.CharField(null=True, blank=True)
    px = models.CharField(null=True, blank=True, default="")
    wo = models.CharField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'WarehouseOrders'

    def __str__(self):
        return str(self.OrderId)
    
@receiver(pre_save, sender=WarehouseOrder)
def set_auto_increment_id(sender, instance, **kwargs):
    if not instance.id:
        max_id = sender.objects.all().aggregate(max_id=models.Max('id'))['max_id']
        instance.id = (max_id or 0) + 1
