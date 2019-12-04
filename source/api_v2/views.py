from rest_framework import viewsets
from .serializers import ProductSerializer, OrderSerializer, OrderProductSerializer
from webapp.models import Product, Order, OrderProduct
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderProductViewSet(viewsets.ModelViewSet):
    serializer_class = OrderProductSerializer
    queryset = OrderProduct.objects.all()
