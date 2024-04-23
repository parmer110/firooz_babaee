from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="created_user", verbose_name="اپراتور", null=True)
    fname = models.CharField(max_length=255, blank=True, null=True, verbose_name="نام کاربر")
    lname = models.CharField(max_length=255, blank=True, null=True, verbose_name="نام خانوادگی")
    username = models.CharField(max_length=255, unique=True, verbose_name="نام کاربری")
    password = models.CharField(max_length=255, verbose_name="رمز عبور")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="تلفن")
    address = models.CharField(max_length=500, blank=True, verbose_name="آدرس")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    Access_Level = (
        ('admin', 'مدیر'),
        ('user', 'کاربر'),
        ('ins', 'بازرس'),
    )
    AccessLevel = models.CharField(choices=Access_Level, max_length=5, null=True, blank=True, verbose_name="سطح دسترسی")

    class Meta:
        db_table = 'WhUsers'  # نام جدول مطابق با SQL Server

    def __str__(self):
        return self.username or ''
