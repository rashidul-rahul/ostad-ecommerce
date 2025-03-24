from django.urls import path
from core.api.v1.orders.views import (
    ShoppingCartDetailAPIView, OrderCreateAPIView, AddToCartAPIView, RemoveFromCartAPIView, OrderDetailAPIView
)


urlpatterns = [
    path('cart/', ShoppingCartDetailAPIView.as_view(), name='shopping-cart-detail'),
    path('cart/add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart/remove/', RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('order/<str:order_id>/', OrderDetailAPIView.as_view(), name='order-detail'),
]