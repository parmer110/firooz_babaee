from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Shipping(models.Model):
 
 shippingTo = models.ForeignKey('companies.company', on_delete=models.CASCADE)
 user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
 date_created=models.DateTimeField(auto_now_add=True )
 date_modified = models.DateTimeField(auto_now=True)









    