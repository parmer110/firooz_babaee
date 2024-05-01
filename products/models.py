from django.db import models
from companies.models import Company

class Product(models.Model):
    id = models.IntegerField(null=True, blank=True, default=0)
    GTIN = models.CharField(max_length=14, primary_key=True, verbose_name='gtin', unique=True)
    ProductFrName = models.CharField(max_length=128, blank=True, null=True)
    irc = models.CharField(max_length=16, null=True, blank=True)
    ProducerCompanyCode = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                            related_name="product_oc", verbose_name='oc', null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Products'

    def __str__(self):
        return self.ProductFrName or ''
