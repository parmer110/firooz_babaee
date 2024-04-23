from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('nationalid', 'companyfaname', 'prefix', 'defaultDc')
    list_editable = ('companyfaname', 'prefix', 'defaultDc')
    list_display_links = ('nationalid',)

    # اضافه کردن فیلترها و جستجو برای بهبود دسترسی و مدیریت
    search_fields = ('nationalid', 'companyfaname')
    list_filter = ('defaultDc', 'prefix')

    # اضافه کردن قابلیت‌های سفارشی‌سازی فرم ادمین
    fieldsets = (
        (None, {
            'fields': ('nationalid', 'companyfaname', 'prefix', 'defaultDc')
        }),
    )
