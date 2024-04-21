from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display=('nid', 'name', 'tel', 'address', 'prefix')
    list_editable=('name', 'tel', 'address', 'prefix')
    list_display_links = None