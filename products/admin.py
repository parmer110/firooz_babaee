from django.contrib import admin
from .models import Product
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('OC', 'name', 'gtin', 'price', 'description', 'image', 'irc', 'datatime_created', 'datatime_modified')

admin.site.register(Product, ProductAdmin)