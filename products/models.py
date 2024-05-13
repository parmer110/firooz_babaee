from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from companies.models import Company

class Product(models.Model):
    id = models.IntegerField(null=True, blank=True, default=0)
    GTIN = models.CharField(max_length=14, primary_key=True, verbose_name='gtin', unique=True)
    ProductFrName = models.CharField(max_length=128, blank=True, null=True)
    irc = models.CharField(max_length=16, null=True, blank=True)
    ProducerCompanyCode = models.ForeignKey(Company, on_delete=models.SET_NULL, 
                                            related_name="product", verbose_name='oc', null=True, db_column="ProducerCompanyCode")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Products'

    def __str__(self):
        return self.ProductFrName or str(self.GTIN)

@receiver(pre_save, sender=Product)
def set_auto_increment_id(sender, instance, **kwargs):
    if not instance.id:
        max_id = sender.objects.all().aggregate(max_id=models.Max('id'))['max_id']
        instance.id = (max_id or 0) + 1
