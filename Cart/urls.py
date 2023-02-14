from django.urls import path
from .views import *

urlpatterns = [
    path('cart-items',GetItemsView.as_view()),
    path('add-item',AddItemView.as_view),
    path('update-item',UpdateItemView.as_view()),
    path('remove-ite,',RemoveItemView.as_view()),
    path('empty-cart',EmptyCartView.as_view()),
    path('synch-cart',SynchCartView.as_view())
]