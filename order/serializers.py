from rest_framework import serializers
# from .models import Inspection
from account.models import CustomUser
from companies.models import  Company
from products.models import  Product
from .models import  tblOrder, XMLFile

class CompanySerializer(serializers.ModelSerializer):
  class Meta:
    model = Company
    fields = "__all__"
class productsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = "__all__"
class tblxmlorderSerializer(serializers.ModelSerializer):
  dc=CompanySerializer()
  class Meta:
    model = XMLFile
    fields = "__all__"
class tblorderSerializer(serializers.ModelSerializer):
  document=tblxmlorderSerializer()
  class Meta:
    model = tblOrder
    fields = "__all__"

class XMLFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = XMLFile
        fields = ['user', 'file', 'uploaded_at']
        read_only_fields = ('user', 'uploaded_at',)

    def validate_file(self, value):
        # بررسی نوع فایل
        if not value.name.endswith('.xml'):
            raise serializers.ValidationError("Only XML files are accepted.")
        return value

