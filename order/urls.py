from unicodedata import name
from django.urls import path
from . import  views

urlpatterns = [
  
     path('UploadFiles/', views.uploadfile,name='UploadFiles'),
   #  path('UploadFiles/', views.FileuploadviewomeView.as_view(),name='UploadFiles'),
     path('show/', views.orders_list_view,name='order_list'),
     path('panel/', views.panel,name='panel'),
     path('<int:pk>/updtepause/', views.updatepause,name='updatepause'),
     path('<int:pk>/updateplay/', views.updateplay,name='updateplay'),
     path('<int:pk>/delete/', views.delete,name='delete'),
     path('',views.panel,name='rooot'), 
     
    
    
    # path('<int:pk>/', views.orders_detail_view,name='order_details'),
    
]
