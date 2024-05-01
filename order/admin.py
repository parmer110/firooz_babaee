from django.contrib import admin
from .models import XMLFile, WarehouseOrder, tblOrder

@admin.register(XMLFile)
class XMLFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'original_file_name', 'file', 'uploaded_at')

@admin.register(WarehouseOrder)
class WarehouseOrderAdmin(admin.ModelAdmin):
    list_display = ('OrderId', 'userId', 'insertdate', 'DistributerCompanyNid', 'deviceid', 'OrderType', 'details')
    search_fields = ('OrderId',)
    list_filter = ('userId', 'DistributerCompanyNid', 'OrderType')

@admin.register(tblOrder)
class tblOrderAdmin(admin.ModelAdmin):
    list_display = ('status', )