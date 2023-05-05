from django.contrib import admin

from .models import Order, OrderBook

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'zip', 'total_price']


@admin.register(OrderBook)
class OrderBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'book', 'price', 'amount']