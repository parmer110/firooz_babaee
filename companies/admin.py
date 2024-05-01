from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('NationalId', 'CompanyFaName', 'Prefix', 'defaultDc')
    list_editable = ('CompanyFaName', 'Prefix', 'defaultDc')
    list_display_links = ('NationalId',)

    search_fields = ('NationalId', 'CompanyFaName')
    list_filter = ('defaultDc', 'Prefix')

    fieldsets = (
        (None, {
            'fields': ('NationalId', 'CompanyFaName', 'Prefix', 'defaultDc')
        }),
    )
