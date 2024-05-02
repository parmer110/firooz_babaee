from django.contrib.auth.decorators import login_required
from logging import exception
from unicodedata import name
from django.http import HttpResponse 
from django.shortcuts import render,reverse,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from config.logging_setup import log_error
import jdatetime
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.exceptions import ObjectDoesNotExist
from order.serializers import XMLFileSerializer
from inquiryHistory import models #for any mode;
from .models import Document
from barcode.models import Barcode
from customer.models import Customer


from products.models import  Product

from django.db.models.functions import Substr, Lower
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import DocumentForm
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from xml.dom.minidom  import parse
import xml.dom.minidom
from itertools import islice
from django.db  import IntegrityError
from django.contrib import messages
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render
from django.views import generic
from .forms import DocumentForm
from django.http import JsonResponse
from .models import tblOrder,XMLFile, WarehouseOrder
from Shipping.models import Shipping
from ShippingDetails.models import ShippingDetail
from rest_framework.authentication import SessionAuthentication

from companies.models import Company
import datetime

from .utils.xml_analyzer import traverse_xml
from account.models import CustomUser



def Save_TC(node):
   rndPack=  str(datetime.datetime.now())
   bulkData=[]
   shipping_instance=[]
   listToAddshipment = []
   uuidpack=''
   parent=''
   order = tblOrder.objects.last()
   shipping_instance = Shipping.objects.last()
   

   
   a=node
   print(a)
   if node.tag=="SP"  :
    uuidpack= node.attrib['PBC'][18:38]  
    if  node.getparent().tag=="SP":
        nodeparent=node.getparent().get("PBC")
        nodeparent=parent[18:38]
    else:
        nodeparent=None
    

   elif node.tag=="ODD" or node.tag=="OD" :
    nodeparent=None
    uuidpack=None
    shipping_instance=Shipping.objects.last()

   for tc in node.findall("TC"):
     OneRow={}
     sh_detail={}
     OneRow['RndEsalat']=tc.attrib["HC"]
     OneRow['UUID']=tc.attrib["BC"][18:38]
     
     
     OneRow['tblOrder']= order
 
     OneRow['parent']=uuidpack
     OneRow['levelid']=0
     sh_detail = ShippingDetail(uid= tc.attrib["BC"][18:38],scanDateTime=datetime.datetime.now(), shipping=shipping_instance)

     bulkData.append(OneRow)
     listToAddshipment.append(sh_detail)

   
  
      # create a ShippingDetail object from the item dictionary
      # append it to the list
      
   if  node.tag!="ODD" and node.tag !="OD" :
     Barcode.objects.create(RndEsalat=rndPack,UUID=uuidpack,order= order,parent=nodeparent,levelid=1)
     ShippingDetail.objects.create(uid= uuidpack,scanDateTime=datetime.datetime.now(), shipping=shipping_instance)
     

   django_list = [Barcode(RndEsalat=row['RndEsalat'],UUID=row['UUID'],order= row['tblOrder'],parent=row['parent'],levelid=row['levelid'])for row in bulkData]
   
   try:
       

       Barcode.objects.bulk_create(django_list) 
       ShippingDetail.objects.bulk_create(listToAddshipment)
       errors={
                    'myerror':'ok',
                    'non':'No',
                        }
   except  IntegrityError as e:
                errors={
                    'myerror':'err',
                    'non':'No',
                        }
                print(e.args)
                barcode =Barcode.objects. filter( pk=order.id)
                barcode.delete()       
                order =tblOrder.objects. filter( pk=order.id)
                order.delete() 
                document=Document.objects.last()
                document.delete()
               
                shipping_instance=Shipping.objects.last()
   
                shipping_instance.delete()
  
                form = DocumentForm()
                return render( 'order/FileUpload.html', {'form': form,'errors': errors})

           

def uploadfile(request):
  errors={
                    'myerror':'get',
                    'non':'No',
                        }
  form={}
  form = DocumentForm(request)
  if request.method == 'POST'  :
    form = DocumentForm(request.POST, request.FILES)

    if form.is_valid():
 
     file = request.FILES["File_addr"]
     t=file.content_type
   
     if t == "text/xml":
        document =  form.save(commit=False)
        document.save()        
        file_name = document.File_addr.name
        xmkdoc=ET.parse(document.File_addr)
        # ÷////÷//////////////////////
        root = xmkdoc.getroot()
        No=root.attrib['NO']
        DC=root.attrib['DC']
        OC=root.attrib['OC']
        LC=root.attrib['LC']
        PX=root.attrib['PX']
        bulkData=[]
        file_addr=file_name
        doc_instance=Document.objects.last()
        companyoc_instance=OC
        companydc_instance=Company.objects.get(nid=DC)
        
        # xml_instance=WarehouseOrder.objects.create(oc=companyoc_instance,dc=companydc_instance, no=No, px=PX,lc =LC, document=doc_instance, User=request.user)
        
        xml_instance = WarehouseOrder.objects.create(
        distributercompanynid=companyoc_instance,
        deviceid=companydc_instance,
        productionorderid=No,
        ordertype=PX,
        details=LC,
        userId=request.user
    )

        shipp_instance= Shipping.objects.create(shippingTo=companydc_instance,user=request.user)
       
        invoicenumber = WarehouseOrder.objects.last()
        product_instance=Product.objects.last()
        for odd in root.findall("ODD"):
      
            MD=odd.get('MD')
            ED=odd.attrib['ED']
            BN=odd.attrib['BN']
            No=odd.attrib['NO']
            LC=odd.attrib['LC']
           
            # for sp in odd.fin("SP"):
            sp=odd.find('SP')
            if sp is not None:
          
             gtin=sp.attrib['PBC'][2:16]
            else: 
             tc= odd.find('TC')
             gtin=tc.attrib['BC'][2:16]
             product_instance=Product.objects.get(gtin=gtin)
             orderid= tblOrder.objects.create(GTIN=product_instance, no=No, md=MD,ed=ED,bn=BN,invoicenumber=invoicenumber)
             Save_TC(odd)  
             continue
           
            orderid= tblOrder.objects.create(GTIN=product_instance, no=No, md=MD,ed=ED,bn=BN,invoicenumber=invoicenumber)
          
            # print ("leel:")
            # print(level)
            # if  level == '2':
            for sp in odd.findall("SP"):
             if sp is not None:
                  level=sp.attrib['PBC'][2:3]
                
              
                  print(level)
                  if level  =='2':
                    Barcode.objects.create(RndEsalat=str(datetime.datetime.now()),UUID=sp.attrib['PBC'][18:38],order= orderid,parent=None,levelid=2)
                    ShippingDetail.objects.create(uid= sp.attrib["PBC"][18:38],scanDateTime=str(datetime.datetime.now()), shipping=shipp_instance)

                    for s_sp in sp.findall("SP"):
                      Save_TC(s_sp)
                  
                  elif level == '1' :           
                    # for s_sp in odd.findall("SP"):#shrink
                       Save_TC(sp)
             else:
                   
                    Save_TC(odd)
               
               
           
          
            
   
  
  return render(request, 'order/FileUpload.html', {'form': form,'errors': errors})

@login_required(login_url='/account/login/')
def orders_list_view(request):
  orders_list=XMLFile.objects.all()

  for order in orders_list:
      order.jalali_date = jdatetime.date.fromgregorian(date=order.uploaded_at.date())

  return render(request,'order/orders_list.html',context={'orders': orders_list})
 


@login_required(login_url='/account/login/')
def panel(request):

   filecount=tblOrder.objects.all().count()
   customercount=Customer.objects.all().count()
   productrcount=Product.objects.all().count()
  #  daycountinquiry/daycodecount)*100
  #  datetime.datetime.now().date().
  #  datetime.date.today()
  #  datetime.datetime.now().time().MidofInquiryPerDay
   MidofInquiryPerDay=60
  
   return render(request,'order/index.html',context={'filecount': filecount,'customercount':customercount,'productrcount':productrcount,'MidofInquiryPerDay':MidofInquiryPerDay})

#def fff(**kwarg) for every input
def delete(request,pk):
    order = get_object_or_404( tblOrder , pk=pk)
    order.delete()
    orders_list= tblOrder .objects.all().values();
    return render(request,'order/orders_list.html',context={'orders': orders_list})
@login_required(login_url='/account/login/')
def updatepause(request,pk):
    # order = get_object_or_404( tblOrder , pk=pk)
     tblOrder .objects.filter(order_id=pk).update(status='dis')
     orders_list= tblOrder .objects.all().values();
     return render(request,'order/orders_list.html',context={'orders': orders_list})

     return render(request, 'blog/post_create.html', context={'form': form})
@login_required(login_url='/account/login/')
def updateplay(request,pk):
    # order = get_object_or_404( tblOrder , pk=pk)
    #  tblOrder .objects.update(status=2)
     tblOrder .objects.filter(order_id=pk).update(status='en')
     orders_list= tblOrder .objects.all().values();
     return render(request,'order/orders_list.html',context={'orders': orders_list})
@login_required(login_url='/account/login/')
def orders_create_view(request):


   pass 
    # if request.method == 'order':
    #     form=UploadFileForm(request.order)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('orders_list')

    # else:
    #     form= NeworderForm()
    # return render(request,'order/order_create.html',context={'form':form})
@login_required(login_url='/account/login/')
def order_update_view(request,pk):

   pass     
    # order = get_object_or_404(order, pk=pk)
    # form=NeworderForm(request.order or None,instance=order)
    # if form.is_valid():
    #     form.save()
    #     return redirect('orders_list')
    # return render(request, 'order/order_create.html', context={'form': form})


class XMLFileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [SessionAuthentication]

    def validate_xml_file(self, file):
        if not file.name.endswith('.xml'):
            return False, "File format is not XML."
        try:
            ET.parse(file)
        except ET.ParseError as e:
            return False, f"XML structure error: {str(e)}"
        return True, ""
    
    def parse_xml(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != 'OD':
            log_error("No OD tag found or XML structure error")
            raise ValueError("No OD tag found or XML structure error")
        
        no = root.get('NO')
        dc = root.get('DC')
        oc = root.get('OC')
        prefix = root.get('PX')
        ot = root.get('OT')
        
        return no, dc, oc, prefix, ot
    
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            log_error("No file provided in the request")
            return Response({"error": "No file inserted!"}, status=status.HTTP_400_BAD_REQUEST)
        
        is_valid, error_message = self.validate_xml_file(file_obj)
        if not is_valid:
            log_error("File validation failed: " + error_message)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        # self.process_and_save_xml(request, file_obj)

        try:
            with transaction.atomic():
                return self.process_and_save_xml(request, file_obj)
        except Exception as e:
            log_error("Error during XML processing: " + str(e))  # Log the exception details
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_or_create_company(self, national_id, prefix=''):
        company, created = Company.objects.get_or_create(
            NationalId=national_id,
            defaults={'Prefix': prefix}
        )
        return company
    
    # @transaction.atomic
    def process_and_save_xml(self, request, file_obj):
        file_obj.seek(0)
        
        no, dc, oc, prefix, ot = self.parse_xml(file_obj)
        
        supplier_company = self.get_or_create_company(oc, prefix=prefix)
        publisher_company = self.get_or_create_company(dc)
        
        data = {
            'NumberOfOrder': int(no) if no.isdigit() else None,
            'SupplierCode': supplier_company,
            'PublisherCode': publisher_company,
            'OrderType': ot if ot else '',
            'original_file_name': file_obj.name,
            'file': file_obj,
            'user': request.user,
        }
        serializer = XMLFileSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            xml_instance = serializer.save()
            file_obj.seek(0)
            tree = ET.parse(file_obj)
            root = tree.getroot()
            result, success = traverse_xml(root, xml_instance)
            if success:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)