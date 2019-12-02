from rest_framework import serializers
from webapp.models import Product, Order, OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'photo', 'category', 'in_order')


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('id', 'order', 'product', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    products = OrderProductSerializer(many=True, read_only=True, source='order_products')

    class Meta:
        model = Order
        fields = ('id', 'user', 'first_name', 'last_name', 'phone', 'email',
                  'products', 'status', 'created_at', 'updated_at')
