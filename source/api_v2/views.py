from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, OrderSerializer, OrderProductSerializer
from webapp.models import Product, Order, OrderProduct
from rest_framework.permissions import SAFE_METHODS, AllowAny, \
    DjangoModelPermissions


class LogoutView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        else:
            return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderProductViewSet(viewsets.ModelViewSet):
    serializer_class = OrderProductSerializer
    queryset = OrderProduct.objects.all()
