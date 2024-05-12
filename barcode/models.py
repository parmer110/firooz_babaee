from django.db import models

class Barcode(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    WhOrderId = models.ForeignKey('order.WarehouseOrder', on_delete=models.CASCADE, null=True,
                             related_name="barcodes", db_column="WhOrderId")
    orderid = models.ForeignKey('order.Orders',on_delete=models.CASCADE, null=True)
    XmlStatus = models.SmallIntegerField(default=0)
    uuid=models.CharField(max_length=20)
    UUIDCount=models.IntegerField(default=0, null=True, blank=True)
    RndEsalat=models.CharField(max_length=140,unique=True, null=True, blank=True)
    RndEsalatCount=models.IntegerField(default=0)
    parent=models.CharField(max_length=20,null=True)
    datatime_created=models.DateTimeField(auto_now_add=True)
    datatime_modified=models.DateTimeField(auto_now=True)
    levelid=models.SmallIntegerField(null=True)

    class Meta:
        db_table = 'Barcodes'

    indexes = [
    models.Index(fields=['RndEsalat',]),
    models.Index(fields=['UUID',]),
]
class ReturningBarcode(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    orderid = models.ForeignKey('order.Orders', on_delete=models.CASCADE, null=True)
    XmlStatus = models.SmallIntegerField(default=0)
    uuid = models.CharField(max_length=20)
    UUIDCount = models.IntegerField(default=0, null=True, blank=True)
    RndEsalat = models.CharField(max_length=140, unique=True, null=True, blank=True)
    RndEsalatCount = models.IntegerField(default=0)
    parent = models.CharField(max_length=20, null=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    levelid = models.SmallIntegerField(null=True)
    whorderid = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Returning_Barcodes'

    indexes = [
        models.Index(fields=['RndEsalat']),
        models.Index(fields=['uuid']),
    ]
