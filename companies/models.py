from django.db import models

class Company(models.Model):
    nationalid = models.CharField(max_length=11, primary_key=True, verbose_name="کدملی شرکت")  # کلید اصلی مطابق با SQL Server
    companyfaname = models.CharField(max_length=128, blank=True, null=True, verbose_name="نام شرکت")
    prefix = models.CharField(max_length=5, null=True, blank=True, verbose_name="پیش کد")
    defaultDc = models.BooleanField(default=False, verbose_name="شرکت پخش پیش‌فرض")  # فیلد Boolean در Node.js مشخص شده است.
    defaultOc = models.BooleanField(default=False, verbose_name="شرکت سفارش‌دهنده پیش‌فرض")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Companies'  # نام جدول مطابق با SQL Server
    
    def __str__(self):
        return self.companyfaname or ''
    
    def save(self, *args, **kwargs):
        if self.defaultDc:
            Company.objects.filter(defaultDc=True).exclude(nationalid=self.nationalid).update(defaultDc=False)
        if self.defaultOc:
            Company.objects.filter(defaultOc=True).exclude(nationalid=self.nationalid).update(defaultOc=False)
        super(Company, self).save(*args, **kwargs)