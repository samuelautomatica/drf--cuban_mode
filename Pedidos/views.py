# from django.shortcuts import render,redirect,HttpResponse
# from Car.Car import Car
# from Car.context_processors import *
# from ShopShein2.settings import EMAIL_HOST_USER
# from .models import Order,OrderItem
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem



# Create your views here.

# @login_required(login_url='/autenticacion/Login')
# def Procesar_Pedido(request):
#     pedido = Pedido.objects.create(user=request.user)
#     car = Car(request)
#     lineas_pedido = list()
#     for key,value in car.car.items:
#         lineas_pedido.append(Linea_Pedido(
#             product_id=key,
#             cantidad = value['cantidad'],
#             user = request.user,
#             pedido_id=pedido,
#         ))
#     Linea_Pedido.objects.bulk_create(lineas_pedido)
#     email_usuario = [request.usermail]
#     #Send_Mail(request,email_usuario)
    

# def Send_Mail(request,email_usuario):

#     context = importe_total_carro(request)
#     precio_total = context['total_dinero']
#     cantidad_total = context['total_elementos']
#     productos = context['lista_productos']
#     subject = 'Detalles del Pedido'
#     message = (f'''
#         Usted ha comprado un total de {cantidad_total} por un valor de {precio_total}
#                                        Productos
#         {productos}
#     ''')
#     email_from = EMAIL_HOST_USER
#     #recipient_list = [str(UserModel.objects.get('email'))]
#     send_mail(subject,message,email_from,email_usuario)
#     messages.error(request,"Pedido realizado con exito")
#     return redirect('modo-cubano/src/components/Product.jsx')


# def Pedidos(request):
#     return HttpResponse("Esta es la pagina de los pedidos")

class ListOrdersView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        try:
            orders = Order.objects.filter(user=user)
            result = []

            for order in orders:
                item = {}
                item['status'] = order.status
                item['transaction_id'] = order.transaction_id
                item['amount'] = order.amount
                item['address_line_1'] = order.address_line_1

                result.append(item)
            
            return Response(
                {'orders': result},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving orders'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListOrderDetailView(APIView):
    def get(self, request, transactionId, format=None):
        user = self.request.user

        try:
            if Order.objects.filter(user=user, transaction_id=transactionId).exists():
                order = Order.objects.get(user=user, transaction_id=transactionId)
                result = {}
                result['status'] = order.status
                result['transaction_id'] = order.transaction_id
                result['amount'] = order.amount
                result['full_name'] = order.full_name
                result['address_line_1'] = order.address_line_1

                order_items = OrderItem.objects.filter(order=order)
                result['order_items'] = []

                for order_item in order_items:
                    sub_item = {}

                    sub_item['name'] = order_item.name
                    sub_item['price'] = order_item.price
                    sub_item['count'] = order_item.count

                    result['order_items'].append(sub_item)
                return Response(
                    {'order': result},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Order with this transaction ID does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving order detail'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )