from .models import Product, Order, OrderItem
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')

        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError('The price must be greater then 0')