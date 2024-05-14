from django.db import models

class Company(models.Model):
    id = models.IntegerField(null=True, blank=True, default=0)
    NationalId = models.CharField(max_length=11, primary_key=True, unique=True)
    CompanyFaName = models.CharField(max_length=128, blank=True, null=True)
    Prefix = models.CharField(max_length=5, null=True, blank=True)
    defaultDc = models.BooleanField(default=False)
    defaultOc = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    Phone = models.CharField(max_length=15, blank=True, null=True)
    Address = models.CharField(max_length=255, blank=True, null=True)
    PostalCode = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'Companies'
    
    def __str__(self):
        return self.CompanyFaName or self.NationalId
    
    def save(self, *args, **kwargs):
        if self.defaultDc:
            Company.objects.filter(defaultDc=True).exclude(nationalid=self.NationalId).update(defaultDc=False)
        if self.defaultOc:
            Company.objects.filter(defaultOc=True).exclude(nationalid=self.NationalId).update(defaultOc=False)
        super(Company, self).save(*args, **kwargs)