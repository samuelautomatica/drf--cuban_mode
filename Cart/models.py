from django.db import models
from Shop.models import ProductModel
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    total_items = models.IntegerField(default=0)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    count = models.IntegerField()