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
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        source='product.price')
    order_by = serializers.CharField(source='order.user.username')

    class Meta:
        model = OrderItem
        fields = [
            'order_by', 
            'product_name', 
            'product_price', 
            'quantity',
            'item_subtotal',
            ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta: 
        model = Order
        fields = [
            'order_id', 
            'user', 
            'created_at', 
            'status', 
            'items', 
            'total_price'
            ]


class ProductInfoSerializer(serializers.Serializer):
    '''Generic Serializer to show products, count, and max_price by subclassing productserializer'''
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
