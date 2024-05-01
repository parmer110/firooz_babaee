from django import forms
from .models import Product
from companies.models import Company  # فرض بر اینکه مدل Company در اپ companies قرار دارد

class ProductForm(forms.ModelForm):
    producercompanycode = forms.ModelChoiceField(queryset=Company.objects.all(), label='شرکت تولید کننده')

    class Meta:
        model = Product
        fields = ['producercompanycode', 'ProductFrName', 'GTIN', 'irc']
