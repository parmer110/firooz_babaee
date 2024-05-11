from django.contrib import admin
from .models import XMLFile, WarehouseOrder, Orders

@admin.register(XMLFile)
class XMLFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'original_file_name', "NumberOfOrder", 'file', 'OrderType', 'SupplierCode', 'PublisherCode', 'createdAt')

@admin.register(Orders)
class tblOrderAdmin(admin.ModelAdmin):
    list_display = ('OrderCode', 'xmlfile_id', 'NumberOfOrder', 'BatchNumber', 'ProductCode', 'ProduceDate', 'ExpDate')

@admin.register(WarehouseOrder)
class WarehouseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'OrderId', 'DistributerCompanyNid', 'ordertype', 'no', 'gtin', 'batchnumber',
                      'expdate', 'userId', 'insertdate', 'ordercompanynid', 'DeviceId', 'productionorderid', 'details',
                        'lc', 'px', 'wo', 'createdAt', 'updatedAt')
    search_fields = ('OrderId',)
    list_filter = ('ordertype',)
