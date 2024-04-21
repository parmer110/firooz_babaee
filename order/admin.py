from django.contrib import admin
from .models import XMLFile, tblXmlOrders, tblOrder

@admin.register(XMLFile)
class XMLFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'original_file_name', 'file', 'uploaded_at')

@admin.register(tblXmlOrders)
class tblXmlOrdersAdmin(admin.ModelAdmin):
    list_display = ('xml_file', 'user', 'oc', 'dc', 'lc', 'no', 'px', 'date_created', 'status')

@admin.register(tblOrder)
class tblOrderAdmin(admin.ModelAdmin):
    list_display = ('invoicenumber','bn', 'md', 'ed', 'sc', 'lc', 'no', 'date_created', 'date_modified', 'status' )