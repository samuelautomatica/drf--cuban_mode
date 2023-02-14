from django.shortcuts import render
from Shop.models import *
from Shop.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


# Create your views here.

# def Home(request):
#     #Carro = Car(request)
#     #context = importe_total_carro(request)
#     #precio_total = context['total_dinero']
#     #cantidad_total = context['total_elementos']
#     #productos = context['lista_productos']
#     #print(precio_total)
#     #print(cantidad_total)
#     #print(productos)
#     product = ProductModel.objects.all()
#     return Response(request,'Shop\Product.jsx',{'product':product})

class Home(APIView):
    def get(self,request,format=None):
        product = ProductModel.objects.all()
        serializer = ProductSerializer(product,many=True)

        return Response({'product':serializer.data},status=status.HTTP_200_OK)
