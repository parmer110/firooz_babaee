from django.contrib import admin
from .models import XMLFile, WarehouseOrder, tblOrder

@admin.register(XMLFile)
class XMLFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'original_file_name', 'file', 'uploaded_at')

@admin.register(WarehouseOrder)
class WarehouseOrderAdmin(admin.ModelAdmin):
    list_display = ('orderid', 'gtin', 'batchnumber', 'expdate', 'userId', 'insertdate', 'lastxmldate', 'distributercompanynid', 'deviceid', 'productionorderid', 'ordertype', 'details')
    search_fields = ('orderid', 'gtin', 'batchnumber')
    list_filter = ('userId', 'distributercompanynid', 'ordertype')

@admin.register(tblOrder)
class tblOrderAdmin(admin.ModelAdmin):
    list_display = ('bn', 'md', 'ed', 'sc', 'lc', 'no', 'date_created', 'date_modified', 'status' )