from django.urls import path
from .views import *

urlpatterns = [
    path('product/<productID',ProductDetailView.as_view())
]