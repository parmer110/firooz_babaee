from django.db import models

class Setting(models.Model):
    subsystem = models.CharField(max_length=50, blank=True, null=True, verbose_name="زیرسیستم")
    attribute = models.CharField(max_length=50, blank=True, null=True, verbose_name="ویژگی")
    value = models.TextField(blank=True, null=True, verbose_name="مقدار")  # nvarchar(255) در SQL Server معادل TextField در Django است
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    class Meta:
        db_table = 'tblSettings'  # اطمینان حاصل کنید که نام جدول با جدول در پایگاه داده SQL Server مطابقت دارد

    def __str__(self):
        return f'{self.subsystem} - {self.attribute} - {self.value}'
