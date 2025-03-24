from django.contrib import admin
from core.apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_date', 'total_cost')
    inlines = [OrderItemInline]
    list_filter = ['status']
