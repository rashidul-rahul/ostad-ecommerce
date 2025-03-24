import uuid
from django.db import models
from django.contrib.auth import get_user_model

from core.apps.products.models import ProductVariant

User = get_user_model()


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, help_text='city/district')
    division = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}, {self.address_line1}, {self.city}"


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"Shopping Cart for {self.user.username}"
        return f"Guest Shopping Cart ({self.session_key})"

    def get_total(self):
        total = sum(item.get_variant_total() for item in self.items.all())
        return total


class ShoppingCartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant}"

    def get_variant_total(self):
        return self.quantity * (self.product_variant.product.base_price or 0)


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
    ]
    order_id = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.address.phone_number}"

    def calculate_total(self):
        total = sum(item.get_line_total() for item in self.order_items.all())
        self.total_cost = total
        self.save()
        return total

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant}"

    def get_line_total(self):
        return self.quantity * self.price