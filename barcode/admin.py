from django.contrib import admin
from .models import Barcode

@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderid', 'levelid', 'uuid', 'UUIDCount', 'RndEsalat', 'RndEsalatCount', 'parent', 'datatime_created', 'datatime_modified')
    search_fields = ('uuid',)
