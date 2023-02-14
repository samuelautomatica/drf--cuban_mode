from django.db import models
from django.contrib.auth import get_user_model
from Shop.models import ProductModel

# Create your models here.

User = get_user_model()

# class Pedido(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.id

#     @property
#     def total(self):
#         return self.lineapedido_set.aggregate(
#             total = Sum(F('price')*('cantidad'),output_field=FloatField)
#         )['total']

#     class Meta:
#         db_table='pedidos'
#         verbose_name = 'pedido'
#         verbose_name_plural = 'pedidos'
#         ordering = ['id']

# class Linea_Pedido(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     product_id = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
#     pedido_id = models.ForeignKey(Pedido,on_delete=models.CASCADE)
#     cantidad = models.IntegerField(default=1)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) :
#         return "f'{self.cantidad}' unidades de {self.product_id.name}"

#     class Meta:
#         db_table='linea_pedidos'
#         verbose_name = 'linea_pedido'
#         verbose_name_plural = 'lineas_pedido'
#         ordering = ['id']

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        not_processed = 'not_processed'
        processed = 'processed'
        delivered = 'delivered'
        cancelled = 'cancelled'
    
    status = models.CharField(
        max_length=50, choices=OrderStatus.choices, default=OrderStatus.not_processed)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    full_name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    

    def __str__(self):
        return self.transaction_id

class OrderItem(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()

    def __str__(self):
        return self.name