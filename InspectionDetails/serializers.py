from rest_framework import serializers
from .models import inspectionDetail
from rest_framework import serializers
from .models import inspectionDetail
from inspections.models import Inspection
from companies.models import  Company
from order.models import  tblOrder, WarehouseOrder as tblXmlOrders
from barcode.models import  Barcode
from products.models import Product
from companies.models import Company
from order.models import tblOrder
class companeisSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Company
    fields = ["nid","name", "tel","address"]
class ProductSerializer(serializers.ModelSerializer):
 OC=companeisSerializer()
 class Meta:
  model = Product
  fields =  ["OC","name", "gtin","irc","price"]



class tblxmlorderSerializer(serializers.ModelSerializer):
  dc=companeisSerializer()
  class Meta:
    model = tblXmlOrders
    fields =  ["oc","dc", "no"]
class tblorderSerializer(serializers.ModelSerializer):
  invoicenumber=tblxmlorderSerializer()
  gtin=ProductSerializer()
  class Meta:
    model = tblOrder
    fields = ["md","ed", "bn","gtin","invoicenumber"]

# Define a BarcodeSerializer class that inherits from ModelSerializer
class BarcodeSerializer(serializers.ModelSerializer):
# Define a Meta class with model and fields attributes
   tblorder=tblorderSerializer()
   class Meta:
    # Set the model attribute to Barcode
     model = Barcode

    # Set the fields attribute to "__all__" to include all fields
     fields = [ 'tblorder']
    
class inspectionDetailSerializer(serializers.ModelSerializer):
  uid=BarcodeSerializer()
  class Meta:
   model = inspectionDetail
   fields = ['Inspection', 'uid', 'scanDateTime']
# class inspectionDetailSerializer(serializers.ModelSerializer):
#  class Meta:
#   model = inspectionDetail
# #   fields = "__all__"
#   fields =  ["id"]

class inspectionDetailSerializer(serializers.ModelSerializer):
  """A serializer for the inspection detail model.

  Attributes:
  uid: A nested serializer for the barcode model.
  """
  uid = BarcodeSerializer()

  class Meta:
    model = inspectionDetail
    fields = ['Inspection', 'uid', 'scanDateTime']

