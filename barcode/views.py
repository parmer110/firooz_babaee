from django.shortcuts import render
import requests
#Import the APIView class, the TokenAuthentication class, and the IsAuthenticated permission class from rest_framework
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse,JsonResponse
# Import the Barcode model and the BarcodeSerializer class from .models and .serializers respectively
from .models import Barcode
from .serializers import BarcodeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import inspectionDetailSerializer, UserSerializer

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def BarcodecreateAPI(request):
 serializer = inspectionDetailSerializer(data=request.data)
 print(serializer)
 if serializer.is_valid():
  inspectionDetail = serializer.save()
  print(serializer.data)
  return Response(serializer.data, status=status.HTTP_201_CREATED)
 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # Define a ScanBarcodeView class that inherits from APIView
class ScanBarcodeView(APIView):
    # Set the authentication_classes attribute to TokenAuthentication
    authentication_classes = [TokenAuthentication]

    # Set the permission_classes attribute to IsAuthenticated
    permission_classes = [IsAuthenticated]

    # Define a post method that takes self, request, and format as parameters
    def post(self, request, format=None):
        # Get the data from the request.data attribute
        data = request.data

        # Create an instance of BarcodeSerializer with data=data and partial=True
        serializer = BarcodeSerializer(data=data, partial=True)

        # Check if the serializer is valid using is_valid() method
        if serializer.is_valid():
            # Save the serializer using save() method
            serializer.save()

            # Return a Response with status code 201 and data=serializer.data
            return Response(serializer.data, status=201)
        else:
        # Return a Response with status code 400 and data=serializer.errors
         return Response(serializer.errors, status=400)
        