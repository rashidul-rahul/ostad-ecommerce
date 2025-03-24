from rest_framework import serializers
from core.apps.orders.models import (
    Address, ShoppingCart, ShoppingCartItem, Order, OrderItem
)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'full_name',
            'address_line1',
            'address_line2',
            'city',
            'division',
            'postal_code',
            'country',
            'phone_number',
        ]


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    product_variant = serializers.StringRelatedField()

    class Meta:
        model = ShoppingCartItem
        fields = ['id', 'product_variant', 'quantity', 'get_variant_total']
        read_only_fields = ['get_variant_total']


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = ShoppingCartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ['id', 'items', 'total']

    def get_total(self, obj):
        return obj.get_total()


class AddToCartSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class RemoveFromCartSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField()


class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'quantity', 'price', 'get_line_total']
        read_only_fields = ['get_line_total']


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'status', 'address', 'total_cost', 'order_items']


class OrderCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'address']
    
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address_instance = Address.objects.create(**address_data)

        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None

        order = Order.objects.create(user=user, address=address_instance, **validated_data)
        return order
