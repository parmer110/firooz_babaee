from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="created_user", verbose_name="اپراتور", null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="تلفن")
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="آدرس")
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updatedAt')
    Access_Level = (
        ('admin', 'مدیر'),
        ('user', 'کاربر'),
        ('ins', 'بازرس'),
    )
    AccessLevel = models.CharField(choices=Access_Level, max_length=10, null=True, blank=True, verbose_name="سطح دسترسی")
    is_staff = models.BooleanField(default=False, null=True, blank=True)
    is_superuser = models.BooleanField(default=False, null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = 'WhUsers'

    def __str__(self):
        return self.username or ''
    
class WhUserToken(models.Model):
    key = models.TextField(blank=True, null=True)
    whUserId = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        null=True,
        db_column='whUserId',
        related_name='tokens'
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'WhUserTokens'