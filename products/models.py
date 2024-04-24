from django.db import models
from companies.models import Company  # فرض بر اینکه مدل Company در اپ companies قرار دارد

class Product(models.Model):
    gtin = models.CharField(max_length=14, primary_key=True, verbose_name='کد جهانی تجاری (GTIN)')
    productfrname = models.CharField(max_length=128, blank=True, null=True, verbose_name='نام فارسی محصول')
    irc = models.CharField(max_length=16, null=True, blank=True, verbose_name='پروانه بهداشتی (IRC)')
    producercompanycode = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='ProducerCompanyCode', verbose_name='شرکت تولید کننده')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Products'  # تنظیم نام جدول مطابق SQL Server

    def __str__(self):
        return self.productfrname or ''
