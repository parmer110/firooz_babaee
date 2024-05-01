from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('ProducerCompanyCode', 'ProductFrName', 'GTIN', 'irc')
    list_display_links = ('GTIN', 'ProductFrName')
    search_fields = ('GTIN', 'ProductFrName')
    list_filter = ('ProducerCompanyCode',)

    fieldsets = (
        (None, {
            'fields': ('GTIN', 'ProductFrName', 'irc', 'ProducerCompanyCode')
        }),
    )
