from django.shortcuts import render,redirect
from .models import inquiryHistory
from barcode.models import Barcode
from products.models import Product
from companies.models import Company
from order.models import tblOrder, WarehouseOrder as tblXmlOrders
from Shipping.models import Shipping
from ShippingDetails.models import ShippingDetail
from InspectionDetails.models import inspectionDetail
from inspections.models import Inspection


from account.models import CustomUser
from .forms import InqueryForm
from django.shortcuts import get_object_or_404
from .serializers import ItemSerializer
from django.shortcuts import render,HttpResponseRedirect,Http404,HttpResponse
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import requests
import json
import datetime
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

def uidinspection(request):
   uuid= request.GET.get('item', None)  
   user = request.user.id
   
   if len(uuid)==20: 
       barcodeinstance=Barcode.objects.filter( UUID=uuid).first()
       if barcodeinstance != None:
        # inspecinstance=Inspection.objects.filter(user_id=user).last() 
        # inspectionDetail.objects.create(Inspection=inspecinstance,uid=barcodeinstance)
        order = get_object_or_404(tblOrder, id=barcodeinstance.order_id)
        # Get the related objects by foreign keys
        orderxml = get_object_or_404(tblXmlOrders, id=order.invoicenumber_id)
        product = get_object_or_404(Product, gtin=order.GTIN_id)
        # shippingDetail = get_object_or_404(ShippingDetail, uid=uuid)
        inspectionJson=[]
        companies=[]
      
        shippingDetails=ShippingDetail.objects.filter(uid=uuid).order_by('date_modified')
        for shippingdetail  in shippingDetails:
            shipping = get_object_or_404(Shipping,id=shippingdetail.shipping_id)
            company=get_object_or_404(Company,nid=shipping.shippingTo_id)
            company_data = {
                              "company": {
                              "name":company.name,
                              "nid": company.nid,
                              "tel": company.tel,
                              "address": company.address
                              }
            }
            companies.append(company_data)


        

        user = get_object_or_404(CustomUser, id=orderxml.User_id)
        # Create a dictionary of the order data
        order_data_array=[]
        order_data = {
        "Order": {
        "id": orderxml.id,
        "mfg": order.md,
        "exp": order.ed,
        "lot": order.bn,
        "product": {
        "irc": product.irc,
        "gtin": product.gtin,
        "name": product.name
        }
        }
        }
        userdata={   
        "user": {
        "id": user.id,
        "fname": user.fname,
        "lname": user.lname,
        "mobile": user.mobile,
        "username": user.username
        
        }
        }
        uiddate={"date": str(datetime.datetime.now())}
        inspectionJson.append(order_data)
        inspectionJson.append(userdata)
        inspectionJson.append( uiddate)
        inspectionJson.append(companies)
        
        
        # order_data_array.append(order_data)
        # Convert the dictionary into a JSON string
        order_json = json.dumps(inspectionJson)
        # Return the JSON response
        return HttpResponse(order_json, content_type="application/json")
       else:
        error={
        "code":"404",
        "msg":"not found,there is no uid with this value:"+uuid
        }
        return HttpResponse(json.dumps(error), content_type="application/json")
      
   else:
      error={
        "code":"404",
        "msg":"stracture error on uid(must be 20 digits).==>"+uuid
        }
      return HttpResponse(json.dumps(error), content_type="application/json")
      # except  IntegrityError as e:  
      #           error={
      #       "code":"404",
      #       "msg":"not found,there is no uid with this value:"+uuid
      #       }
  #  return HttpResponse(json.dumps(error), content_type="application/json")
       
        
def show_inquiry_form(request):
      item={}    
      return render( request,'inquiryHistory/inquiry.html',{'item': item})
 
 
def uuidInquiryToInspection(request):
        
       if request.GET.get('isuid')=='yes'  :
         item={}  
         row=[]
         Order_row=[]
         orderXml_row=[]
         product_row=[]
         company_row=[]
         user_row=[]
         
         
         uuid = request.GET.get('item', None)   
         row=Barcode.objects.filter(UUID=uuid).first()
         if row  :
              Order_row=tblOrder.objects.filter(orderid=row.tblOrder).first()
              Orderxml_row=tblOrder.objects.filter(id=Order_row.invoicenumber).first()
              product_row=Product.objects.filter(GTIN=Order_row.gtin).first()
              company_row=Company.objects.filter(nid=Orderxml_row.oc).first()
              user_row=CustomUser.objects.filter(id=Orderxml_row.user).first()
  #             [{"id":"452577",
  # "uid":"21996000013398957740",
  # "Order":{"id":"452578","mfg":"2005-07-22","exp":"1991-03-15","lot":"58073",
  # "product":{"id":"452579","gtin":"68381196592651","name":"RIENZI"}},
  # "from":{"id":"452495","name":"Mae Richie","nid":"46122682651","address":"1250 Whitewater, Kaneohe, Georgia, 65340","phone":"+968-6649-885-125","mobile":"+504-6767-942-487",
  # "location":{"id":"452496","latitude":"65.0243","longitude":"-88.4420"}},
  # "to":{"id":"452499","name":"Celina Easley","nid":"69027369802","address":"6112 Edgars, Springfield, Indiana, 72993","phone":"+32-8755-762-980","mobile":"+501-4437-652-506",
  # "location":{"id":"452500","latitude":"51.2454","longitude":"35.5409"}},
  # "user":{"id":"452494","fname":"Leeann","lname":"Strong","mobile":"+92-9288-032-156","username":"erma.mcmillan2940@anyone.com","password":"friend"},"date":"2022-04-17 17:56:10"}]
              
              item={
                'uuid':row.UUID
                
              }
              data={
                'items':item
              }
         else :  
            item={
                'uuid':''
              }
            data={
                'items':item
              }       
         
         return JsonResponse(data)    
def uuidInquiry(request):
        
       if request.GET.get('isuid')=='yes'  :
         item={}  
         row=[]
         uuid = request.GET.get('item', None)   
         row=Barcode.objects.filter(UUID=uuid).first()
         if row  :
            
              item={
                'uuid':row.UUID
              }
              data={
                'items':item
              }
         else :  
            item={
                'uuid':''
              }
            data={
                'items':item
              }       
         
         return JsonResponse(data)
            
def RndEsalatInquiry(request):
     if request.GET.get('isuid')=='no' :
         vitem={}  
         row=[]
         rndesalat = request.GET.get('item', None)  
         rndesalat=  hashlib.sha1(rndesalat.encode('utf-8')).hexdigest().upper()
         row=Barcode.objects.filter(RndEsalat=rndesalat).first()
         if row :
              item={
                'uuid':row.RndEsalat
              }
              data={
                'items':item
              }
         else :  
            item={
                'uuid':''
              }
            data={
                'items':item
              }  
         
         return JsonResponse(data)   


def RndEsalatInquirySMS(rndesalat,frm):
     result=""
     if len(rndesalat)==20 :
        # rndesalat=hashlib.sha1(rndesalat.encode('utf-8')).hexdigest().upper()      
         row=Barcode.objects.filter(UUID=rndesalat).first()
         if row :
           result="ok"
         else:
           result="len"
     return result
     
              
def getSMS(request):
    
    udh = str(request.GET.get('udh'))
    frm = str(request.GET.get('from'))
    text = str(request.GET.get('text'))
       # list=text.split("*")
    # if len(list)== 4:
    #     name=list[0]
    #     location=list[1]
    #     job=list[2]
    #     HC=list[3]
        #HC= hashlib.sha1(rndesalat.encode('utf-8')).hexdigest().upper()
        
    rndesalat=RndEsalatInquirySMS(text,frm)
    print(rndesalat)
    if rndesalat =="ok" :
        text="اصالت کالا مورد تایید است"
    elif rndesalat =="len" :  
        text="طول کد ارسالی نامعتبر است"
    else:
         text="اصالت کالا مورد تایید نیست"    
    sendSmsViaGet (text,frm)
    return HttpResponse(text )

   
def sendSMS(text,to):
    #
    # Python samples are made with Requests: HTTP for Humans
    #
    # https://requests.readthedocs.io/en/master/
    #
    url = "https://sms.magfa.com/api/http/sms/v2/send"
    headers = {'accept': "application/json", 'cache-control': "no-cache"}
    # credentials
    username = "hamgam_611"
    password = "DQT7VCZXTLPpHZTz"
              #"AjMvGHQJ5eFCNAC"
    domain = "magfa"

    # data
    #  payload_tuples = [('senders': '3000611'), ( 'messages':text),( 'recipients':to)]
   
    # call post form data
    
    # response = requests.post(url, headers=headers, auth=(username + '/' + domain, password), data=payload_tuples)

    # or json data
    payload_json = {'senders': ['3000611'], 'messages':[text], 'recipients':[to],}
    # call json
    response = requests.post(url, headers=headers, auth=(username + '/' + domain, password), json=payload_json)
    print(response.json())

def sendSmsViaGet(text,frm):
  # https://requests.readthedocs.io/en/master/
    # credentials
  username = "hamgam_611"
  password = "DQT7VCZXTLPpHZTz"
              #"AjMvGHQJ5eFCNAC"
  domain = "magfa"

  # call
  contents = requests.get("https://sms.magfa.com/api/http/sms/v1?service=enqueue&username=" + username + "&password=" + password + "&domain=" + domain + "&from=983000611&to="+frm+"&text="+text);
  
def getstatuse(request):
    #
    # Python samples are made with Requests: HTTP for Humans
    #
    # https://requests.readthedocs.io/en/master/
    #
  

    mid = 12345
    url = "https://sms.magfa.com/api/http/sms/v2/statuses/" + mid
    headers = {'accept': "application/json", 'cache-control': "no-cache"}

    username = "hamgam_611"
    password = "AjMvGHQJ5eFCNAC"
    # "1@2345678"
    # AjMvGHQJ5eFCNAC
    domain = "magfa"

    # call
    response = request.get(url, headers=headers, auth=(username + '/' + domain, password))
    print(response.json())

