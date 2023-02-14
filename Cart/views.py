from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart,CartItem
from Shop.models import ProductModel
from Shop.serializers import ProductSerializer

# Create your views here.

class GetItemsView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)

            result = []

            if CartItem.objects.filter(cart=cart).exists():
                for cart_item in cart_items:
                    item = {}

                    item['id'] = cart_item.id
                    item['count'] = cart_item.count
                    product = ProductModel.objects.get(id=cart_item.product.id)
                    product = ProductSerializer(product)

                    item['product'] = product.data

                    result.append(item)
            return Response({'cart': result}, status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'Something went wrong when retrieving cart items'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddItemView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        count = 1

        try:
            if not ProductModel.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exist'},
                    status=status.HTTP_404_NOT_FOUND)
            
            product = ProductModel.objects.get(id=product_id)
            
            cart = Cart.objects.get(user=user)

            if CartItem.objects.filter(cart=cart, product=product).exists():
                return Response(
                    {'error': 'Item is already in cart'},
                    status=status.HTTP_409_CONFLICT)

            if int(product.quantity) > 0:
                CartItem.objects.create(
                    product=product, cart=cart, count=count
                )

                if CartItem.objects.filter(cart=cart, product=product).exists():
                    total_items = int(cart.total_items) + 1
                    Cart.objects.filter(user=user).update(
                        total_items=total_items
                    )
                
                    cart_items = CartItem.objects.filter(cart=cart)

                    result = []

                    for cart_item in cart_items:

                        item = {}
                        item['id'] = cart_item.id
                        item['count'] = cart_item.count
                        product = ProductModel.objects.get(id=cart_item.product.id)
                        product = ProductSerializer(product)

                        item['product'] = product.data

                        result.append(item)

                    return Response({'cart': result}, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {'error': 'Not enough of this item in stock'},
                        status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'Something went wrong when adding item to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateItemView(APIView):
    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)
        
        try:
            count = int(data['count'])
        except:
            return Response(
                {'error': 'Count value must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        try:
            if not ProductModel.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exist'},
                    status=status.HTTP_404_NOT_FOUND)
            
            product = ProductModel.objects.get(id=product_id)
            cart = Cart.objects.get(user=user)

            if not CartItem.objects.filter(cart=cart, product=product).exists():
                return Response(
                    {'error': 'This product is not in your cart'},
                    status=status.HTTP_404_NOT_FOUND)
            
            quantity = product.quantity

            if count <= quantity:
                CartItem.objects.filter(
                    product=product, cart=cart
                ).update(count=count)

                cart_items = CartItem.objects.order_by(
                    'product').filter(cart=cart)

                result = []

                for cart_item in cart_items:
                    item = {}

                    item['id'] = cart_item.id
                    item['count'] = cart_item.count
                    product = ProductModel.objects.get(id=cart_item.product.id)
                    product = ProductSerializer(product)

                    item['product'] = product.data

                    result.append(item)

                return Response({'cart': result}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Not enough of this item in stock'},
                    status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'Something went wrong when updating cart item'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RemoveItemView(APIView):
    def delete(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)
        
        try:
            if not ProductModel.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exist'},
                    status=status.HTTP_404_NOT_FOUND)
            
            product = ProductModel.objects.get(id=product_id)
            cart = Cart.objects.get(user=user)

            if not CartItem.objects.filter(cart=cart, product=product).exists():
                return Response(
                    {'error': 'This product is not in your cart'},
                    status=status.HTTP_404_NOT_FOUND)
            
            CartItem.objects.filter(cart=cart, product=product).delete()

            if not CartItem.objects.filter(cart=cart, product=product).exists():
                # actualizar numero total en el carrito
                total_items = int(cart.total_items) - 1
                Cart.objects.filter(user=user).update(total_items=total_items)

            cart_items = CartItem.objects.filter(cart=cart)

            result = []

            if CartItem.objects.filter(cart=cart).exists():
                for cart_item in cart_items:
                    item = {}

                    item['id'] = cart_item.id
                    item['count'] = cart_item.count
                    product = ProductModel.objects.get(id=cart_item.product.id)
                    product = ProductSerializer(product)

                    item['product'] = product.data

                    result.append(item)

            return Response({'cart': result}, status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'Something went wrong when removing item'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmptyCartView(APIView):
    def delete(self, request, format=None):
        user = self.request.user

        try:
            cart = Cart.objects.get(user=user)

            if not CartItem.objects.filter(cart=cart).exists():
                return Response(
                    {'success': 'Cart is already empty'},
                    status=status.HTTP_200_OK)

            CartItem.objects.filter(cart=cart).delete()

            # Actualizamos carrito
            Cart.objects.filter(user=user).update(total_items=0)

            return Response(
                {'success': 'Cart emptied successfully'},
                status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'Something went wrong emptying cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SynchCartView(APIView):
    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            cart_items = data['cart_items']

            for cart_item in cart_items:
                cart = Cart.objects.get(user=user)

                try:
                    product_id = int(cart_item['product_id'])
                except:
                    return Response(
                        {'error': 'Product ID must be an integer'},
                        status=status.HTTP_404_NOT_FOUND)

                if not ProductModel.objects.filter(id=product_id).exists():
                    return Response(
                        {'error': 'Product with this ID does not exist'},
                        status=status.HTTP_404_NOT_FOUND)

                product = ProductModel.objects.get(id=product_id)
                quantity = product.quantity

                if CartItem.objects.filter(cart=cart, product=product).exists():
                    # Actualiizamos el item del carrito
                    item = CartItem.objects.get(cart=cart, product=product)
                    count = item.count

                    try:
                        cart_item_count = int(cart_item['count'])
                    except:
                        cart_item_count = 1

                    #Chqueo con base de datos
                    if (cart_item_count + int(count)) <= int(quantity):
                        updated_count = cart_item_count + int(count)
                        CartItem.objects.filter(
                            cart=cart, product=product
                        ).update(count=updated_count)
                else:
                    #Agregar el item al carrito del usuario
                    try:
                        cart_item_count = int(cart_item['count'])
                    except:
                        cart_item_count = 1

                    if cart_item_count <= quantity:
                        CartItem.objects.create(
                            product=product, cart=cart, count=cart_item_count
                        )

                        if CartItem.objects.filter(cart=cart, product=product).exists():
                            #Sumar item
                            total_items = int(cart.total_items) + 1
                            Cart.objects.filter(user=user).update(
                                total_items=total_items
                            )

                return Response(
                {'success': 'Cart Synchronized'},
                status=status.HTTP_201_CREATED)
        except:
            return Response(
                {'error': 'Something went wrong when synching cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)