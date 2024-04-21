from email.policy import default
from typing import Any
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.deconstruct  import deconstructible
from django.core.validators import MaxLengthValidator, MinLengthValidator
from order.utils.file_utils import unique_file_name
from account.models import CustomUser


# class XmlValidator:
#     def __call__(self, value):
#         ext=value.name.split('.')[-1].lower()
#         if ext != 'xml':
#             raise ValidationError('Only XML files are allowed.')

# validate_xml = XmlValidator()

class Document(models.Model):
  
    File_addr = models.FileField(upload_to='XmlFiles/%Y/%m/%d/',verbose_name='انتخاب فایل')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
    
class tblXmlOrders (models.Model):
    STATUS_CHOICES=(
     ('en','قابل استعلام'),
     ('dis','غیرقابل استعلام'),
    )
    xml_file = models.ForeignKey('XMLFile',on_delete=models.CASCADE,null=True)
    user=models.ForeignKey('account.CustomUser',on_delete=models.CASCADE,null=True)
    oc=models.ForeignKey('companies.Company', on_delete=models.SET_NULL, null=True, related_name="OD")
    dc=models.ForeignKey('companies.Company',on_delete=models.CASCADE,null=True)
    lc=models.CharField(max_length=11)
    no=models.PositiveIntegerField()
    px=models.PositiveIntegerField()
    date_created=models.DateTimeField(auto_now_add=True )
    date_modified = models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=3,default='dis', choices=STATUS_CHOICES)
    def __str__(self):
         return str(self. id)

class tblOrder (models.Model):
    STATUS_CHOICES=(
     ('en','قابل استعلام'),
     ('dis','غیرقابل استعلام'),
     )

    invoicenumber=models.ForeignKey('order.tblXmlOrders',on_delete=models.CASCADE)
    GTIN=models.ForeignKey('products.Product',on_delete=models.CASCADE, null=True)
    bn=models.CharField(max_length=14)
    md = models.CharField(
        # verbose_name="تاریخ تولید",
        max_length=10,
        validators=[
            MinLengthValidator(10),
        ]
    )
    ed = models.CharField(
        # verbose_name="تاریخ انقضا",
        max_length=10,
        validators=[
            MinLengthValidator(10),
        ]
    )
    sc = models.CharField(max_length=20, verbose_name="IRC")
    lc = models.CharField(max_length=20, null=True)
    no=models.PositiveIntegerField()
   
    date_created=models.DateTimeField(auto_now_add=True )
    date_modified = models.DateTimeField(auto_now=True)
    status=models.CharField(STATUS_CHOICES,max_length=3,default='dis')
#     indexes = [
#     models.Index(fields=[' id',]),
   
# ]
 
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
 
    
    


