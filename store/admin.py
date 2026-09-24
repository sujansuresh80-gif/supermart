from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'stock',
        'created_at',
    )

    search_fields = (
        'name',
        'category',
    )

    list_filter = (
        'category',
        'created_at',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'order_date',
        'status',
    )

    search_fields = (
        'user__username',
    )

    list_filter = (
        'status',
        'order_date',
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
        'total_price',
    )

    search_fields = (
        'product__name',
        'order__user__username',
    )