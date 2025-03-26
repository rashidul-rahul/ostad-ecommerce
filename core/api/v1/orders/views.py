from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.apps.orders.models import ShoppingCart, ShoppingCartItem, Order, OrderItem
from core.apps.orders.serializers import (
    ShoppingCartSerializer,
    AddToCartSerializer,
    RemoveFromCartSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer,
    )


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = ShoppingCart.objects.get_or_create(session_key=session_key, user=None)
    return cart



class ShoppingCartDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = []  # Allow both authenticated and guest users

    def get_object(self):
        request = self.request
        if request.user.is_authenticated:
            cart, created = ShoppingCart.objects.get_or_create(user=request.user)
            return cart
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = ShoppingCart.objects.get_or_create(session_key=session_key, user=None)
            return cart


class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = []

    def perform_create(self, serializer):
        request = self.request
        user = request.user if request.user.is_authenticated else None
        cart = get_or_create_cart(request)
        
        # Create the order (this creates the address as well)
        order = serializer.save(user=user)
        
        # Loop through cart items to create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_variant=cart_item.product_variant,
                quantity=cart_item.quantity,
                price=cart_item.product_variant.product.base_price  # or however you determine the price
            )
        
        # Optionally update order total if needed
        order.calculate_total()
        
        # Clear the shopping cart
        cart.items.all().delete()


class AddToCartAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_variant_id = serializer.validated_data['product_variant_id']
        quantity = serializer.validated_data['quantity']

        cart = get_or_create_cart(request)

        cart_item, created = ShoppingCartItem.objects.get_or_create(
            shopping_cart=cart, product_variant_id=product_variant_id
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return Response({'detail': 'Item added to cart.'}, status=status.HTTP_200_OK)


class RemoveFromCartAPIView(APIView):
    permission_classes = []  # Allow both guest and authenticated users

    def post(self, request, *args, **kwargs):
        serializer = RemoveFromCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_variant_id = serializer.validated_data['product_variant_id']

        cart = get_or_create_cart(request)
        try:
            cart_item = ShoppingCartItem.objects.get(shopping_cart=cart, product_variant_id=product_variant_id)
            cart_item.delete()
            return Response({'detail': 'Item removed from cart.'}, status=status.HTTP_200_OK)
        except ShoppingCartItem.DoesNotExist:
            return Response({'detail': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'order_id'
    permission_classes = [permissions.AllowAny]
