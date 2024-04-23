from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('producercompanycode', 'productfrname', 'gtin', 'irc')
    list_display_links = ('gtin', 'productfrname')
    search_fields = ('gtin', 'productfrname')
    list_filter = ('producercompanycode',)

    fieldsets = (
        (None, {
            'fields': ('gtin', 'productfrname', 'irc', 'producercompanycode')
        }),
    )
