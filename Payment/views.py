from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Cart.models import Cart, CartItem
from Pedidos.models import Order, OrderItem
from Shop.models import ProductModel
from django.core.mail import send_mail
import braintree

# Create your views here.

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=settings.BT_ENVIRONMENT,
        merchant_id=settings.BT_MERCHANT_ID,
        public_key=settings.BT_PUBLIC_KEY,
        private_key=settings.BT_PRIVATE_KEY
))

class GetPaymentTotalView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        try:
            cart = Cart.objects.get(user=user)

            #revisar si existen items
            if not CartItem.objects.filter(cart=cart).exists():
                return Response(
                    {'error': 'Need to have items in cart'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            cart_items = CartItem.objects.filter(cart=cart)

            for cart_item in cart_items:
                if not ProductModel.objects.filter(id=cart_item.product.id).exists():
                    return Response(
                        {'error': 'A proudct with ID provided does not exist'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                if int(cart_item.count) > int(cart_item.product.quantity):
                    return Response(
                        {'error': 'Not enough items in stock'},
                        status=status.HTTP_200_OK
                    )
                
                total_amount = 0.0

                for cart_item in cart_items:
                    total_amount += (float(cart_item.product.price) * float(cart_item.count))
                
                total_amount = round(total_amount, 2)

                return Response({
                    'total_amount': f'{total_amount:.2f}',
                },
                    status=status.HTTP_200_OK
                )

        except:
            return Response(
                {'error': 'Something went wrong when retrieving payment total information'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProcessPaymentView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data

        nonce = data['nonce']
        full_name = data['full_name']
        address_line_1 = data['address_line_1']
        
        cart = Cart.objects.get(user=user)

        #revisar si usuario tiene items en carrito
        if not CartItem.objects.filter(cart=cart).exists():
            return Response(
                {'error': 'Need to have items in cart'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        cart_items = CartItem.objects.filter(cart=cart)

        # revisar si hay stock

        for cart_item in cart_items:
            if not ProductModel.objects.filter(id=cart_item.product.id).exists():
                return Response(
                    {'error': 'Transaction failed, a proudct ID does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            if int(cart_item.count) > int(cart_item.product.quantity):
                return Response(
                    {'error': 'Not enough items in stock'},
                    status=status.HTTP_200_OK
                )
        
        total_amount = 0.0

        for cart_item in cart_items:
            total_amount += (float(cart_item.product.price) * float(cart_item.count))

        total_amount = round(total_amount, 2)

        #Crear transaccion con braintree
        try:
            newTransaction = gateway.transaction.sale(
                {
                    'amount':str(total_amount),
                    'payment_method_nonce':str(nonce['nonce']),
                    'options':{
                        'submit_for_settlement': True
                    }
                }
            )
        except :
            return Response(
                {'error':'Error procesing the transacstion'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if newTransaction.is_success or newTransaction.transaction:
            for cart_item in cart_items:
                update_product = ProductModel.objects.get(id=cart_item.product.id)

                #encontrar cantidad despues de coompra
                quantity = int(update_product.quantity) - int(cart_item.count)

                # #obtener cantidad de producto por vender
                # sold = int(update_product.sold) + int(cart_item.count)

                #actualizar el producto
                ProductModel.objects.filter(id=cart_item.product.id).update(
                    quantity=quantity,
                )
            
            #crear orden
            try:
                order = Order.objects.create(
                    user=user,
                    transaction_id=newTransaction.transaction.id,
                    amount=total_amount,
                    full_name=full_name,
                    address_line_1 = address_line_1
                    )
            except:
                    return Response(
                        {'error': 'Transaction succeeded but failed to create the order'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            
            for cart_item in cart_items:
                try:
                    # agarrar el producto
                    product = ProductModel.objects.get(id=cart_item.product.id)

                    OrderItem.objects.create(
                        product=product,
                        order=order,
                        name=product.name,
                        price=cart_item.product.price,
                        count=cart_item.count
                    )
                except:
                    return Response(
                        {'error': 'Transaction succeeded and order created, but failed to create an order item'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            try:
                send_mail(
                    'Your Order Details',
                    'Hey ' + full_name + ','
                    + '\n\nWe recieved your order!'
                    + '\n\nGive us some time to process your order and ship it out to you.'
                    + '\n\nYou can go on your user dashboard to check the status of your order.'
                    + '\n\nSincerely,'
                    + '\nShop Time',
                    '**************',
                    [user.email],
                    fail_silently=False
                )
            except:
                return Response(
                    {'error': 'Transaction succeeded and order created, but failed to send email'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            try:
                # Vaciar carrito de compras
                CartItem.objects.filter(cart=cart).delete()

                # Actualizar carrito
                Cart.objects.filter(user=user).update(total_items=0)
            except:
                return Response(
                    {'error': 'Transaction succeeded and order successful, but failed to clear cart'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response(
                {'success': 'Transaction successful and order was created'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Transaction failed'},
                status=status.HTTP_400_BAD_REQUEST
            )