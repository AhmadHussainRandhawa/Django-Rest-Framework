from .models import Product, Order, OrderItem
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('The price must be greater then 0')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta: 
        model = Order
        fields = ['order_id', 'user', 'created_at', 'status', 'items']



        