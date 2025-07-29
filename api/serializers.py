from .models import Product, Order, OrderItem
from rest_framework import serializers
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('The price must be greater then 0')
        return value  


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
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True)
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


class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderWriteSerializer(serializers.ModelSerializer):
    items = OrderItemWriteSerializer(many=True)
    order_id = serializers.UUIDField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        order_items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in order_items:
            OrderItem.objects.create(order=order,**item)
        return order

    def update(self, instance, validated_data):
        order_items = validated_data.pop('items', None)

        with transaction.atomic():
            # Update main Order fields using DRF's default logic
            instance = super().update(instance, validated_data)

            if order_items is not None:
                instance.items.all().delete()
                for item in order_items:
                    OrderItem.objects.create(order=instance, **item)
        return instance

    class Meta:
        model = Order
        fields = [
            'order_id',
            'user',
            'status',
            'items',
        ]


class ProductInfoSerializer(serializers.Serializer):
    '''Generic Serializer to show products, count, and max_price by subclassing productserializer'''
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()


'''         # 2nd Approach for Order Serializer


class OrderItemReadSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price'
    )
    order_by = serializers.CharField(source='order.user.username')
    item_subtotal = serializers.SerializerMethodField()

    def get_item_subtotal(self, obj):
        return obj.product.price * obj.quantity

    class Meta:
        model = OrderItem
        fields = [
            'order_by',
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal'
        ]


class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    total_price = serializers.SerializerMethodField()
    
    # Use read serializer for reading, write serializer for writing
    items = OrderItemReadSerializer(many=True, read_only=True)
    item_inputs = OrderItemWriteSerializer(many=True, write_only=True)

    def get_total_price(self, obj):
        return sum(item.item_subtotal for item in obj.items.all())

    def create(self, validated_data):
        items_data = validated_data.pop('item_inputs')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    class Meta:
        model = Order
        fields = [
            'order_id',
            'user',
            'created_at',
            'status',
            'items',         # For reading
            'item_inputs',   # For writing
            'total_price'
        ]
'''