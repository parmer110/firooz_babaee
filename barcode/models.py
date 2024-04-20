from django.db import models

class Barcode(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
   
    order=models.ForeignKey('order.tblOrder',on_delete=models.CASCADE)

    UUID=models.CharField(max_length=20,unique=True)
    UUIDCount=models.IntegerField(default=0)
    RndEsalat=models.CharField(max_length=140,unique=True)
    RndEsalatCount=models.IntegerField(default=0)
    parent=models.CharField(max_length=20,null=True)
    datatime_created=models.DateTimeField(auto_now_add=True)
    datatime_modified=models.DateTimeField(auto_now=True)
    levelid=models.SmallIntegerField(null=True)
    
    
    indexes = [
    models.Index(fields=['RndEsalat',]),
    models.Index(fields=['UUID',]),
]
