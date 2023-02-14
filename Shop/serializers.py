from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    # img = serializers.CharField(source='get_image')
    class Meta:
        model = ProductModel
        fields = [
            'id',
            'name',
            'price',
            'image',
            'description',
            'quantity',
            'get_image'
        ]