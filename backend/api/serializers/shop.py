from rest_framework import serializers
from api.models.shop import Product, Cart, CartItem, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'description_short', 'description_long',
            'price', 'old_price', 'image', 'gallery', 'rating', 'stock',
            'brand', 'features', 'recommended_for', 'is_in_stock', 'discount_percentage',
            'created_at', 'updated_at'
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'created_at']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    total_items = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'total_items', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'shipping_address', 'shipping_city',
            'shipping_postal_code', 'shipping_country', 'total_price', 'shipping_cost',
            'status', 'created_at', 'updated_at', 'shipped_at', 'delivered_at', 'items'
        ]
        read_only_fields = ['order_number', 'user']
