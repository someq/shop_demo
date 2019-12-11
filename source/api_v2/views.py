from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .serializers import ProductSerializer, OrderSerializer, OrderProductSerializer, UserSerializer, \
    UserRegisterSerializer
from webapp.models import Product, Order, OrderProduct
from rest_framework.permissions import SAFE_METHODS, AllowAny, \
    DjangoModelPermissions, BasePermission


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

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('webapp.change_order'):
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)


class OrderProductViewSet(viewsets.ModelViewSet):
    serializer_class = OrderProductSerializer
    queryset = OrderProduct.objects.all()


class RegisterApiView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(instance=user).data)
        response = Response(serializer.errors)
        response.status_code = 400
        return response
