# models.py
from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
   

    name = models.CharField(max_length=255,verbose_name="نام شرکت")
    tel = models.CharField(max_length=20,verbose_name="تلفن")
    address = models.CharField(max_length=255,verbose_name="آدرس")
    nid = models.CharField(primary_key=True, max_length=11,verbose_name="کدملی شرکت", editable=True)
    prefix = models.CharField(max_length=5,null=True,blank=True,verbose_name="پیش کد")
    latitude=models.CharField(max_length=50,null=True)
    longitude=models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
         return str(self. name)






