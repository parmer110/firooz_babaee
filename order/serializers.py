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
class XMLFileSerializer(serializers.ModelSerializer):
    SupplierCode = serializers.CharField()
    PublisherCode = serializers.CharField()
    OrderType = serializers.ChoiceField(
        choices=XMLFile.ORDER_TYPE,
        required=False,
        allow_blank=True,
        allow_null=True
    )
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = XMLFile
        fields = ['id', 'NumberOfOrder', 'SupplierCode', 'PublisherCode', 'OrderType', 
                  'user', 'original_file_name', 'file', 'createdAt', 'error_message', 
                  'status', 'createdAt', 'updatedAt']
        read_only_fields = ('user', 'createdAt', 'status', 'createdAt', 'updatedAt')

    def validate_file(self, value):
        if not value.name.endswith('.xml'):
            raise serializers.ValidationError("Only XML files are accepted.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        supplier_code = validated_data.pop('SupplierCode')
        publisher_code = validated_data.pop('PublisherCode')

        supplier_company, created = Company.objects.get_or_create(NationalId=supplier_code)
        publisher_company, created = Company.objects.get_or_create(NationalId=publisher_code)
        
        validated_data['SupplierCode'] = supplier_company
        validated_data['PublisherCode'] = publisher_company

        instance = XMLFile.objects.create(user=user, **validated_data)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['SupplierCode'] = instance.SupplierCode.NationalId if instance.SupplierCode else None
        rep['PublisherCode'] = instance.PublisherCode.NationalId if instance.PublisherCode else None
        return rep