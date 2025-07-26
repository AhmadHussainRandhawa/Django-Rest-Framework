from django.contrib import admin
from .models import Product, Order, OrderItem


# User TabularInline when you want to include child table in parent
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)

