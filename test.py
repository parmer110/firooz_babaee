from django.db import models
from django.contrib.auth.models import AbstractUser

class WhUsers(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)