# from django.shortcuts import render,HttpResponse

# #from Cart.context_processors import importe_total_carro
# from .models import *
# #from Car.Car import Car

# # Create your views here.

# def Shop(request):
#     #Carro = Car(request)
#     context = importe_total_carro(request)
#     precio_total = context['total_dinero']
#     cantidad_total = context['total_elementos']
#     productos = context['lista_productos']
#     print(precio_total)
#     print(cantidad_total)
#     print(productos)
#     product = ProductModel.objects.all()
#     return render(request,'Shop\Product.jsx',{'product':product})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import ProductModel
from .serializers import ProductSerializer


class ProductDetailView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        try:
            product_id=int(productId)
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)
        
        if ProductModel.objects.filter(id=product_id).exists():
            product = ProductModel.objects.get(id=product_id)

            product = ProductSerializer(product)

            return Response({'product': product.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Product with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)