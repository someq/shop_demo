from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from webapp.models import Product, Order, OrderProduct, CATEGORY_CHOICES


class ProductSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(required=False, read_only=True, source='get_category_display')

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'photo', 'category', 'in_order', 'category_display')


# Оставлено для примера некоторых полей сериализаторов
# используйте этот класс вместо вышеописанного ProductSerializer,
# но учтите, что он не умеет создавать и обновлять объекты.

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=200, required=True)
#     category = serializers.ChoiceField(choices=CATEGORY_CHOICES, required=True, write_only=True)
#     category_display = serializers.CharField(required=False, read_only=True, source='get_category_display')
#     photo = serializers.ImageField(required=False, allow_null=True)
#     price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
#     in_order = serializers.BooleanField(default=True)
#
#     check = serializers.SerializerMethodField(read_only=True, method_name='get_check')
#
#     def get_check(self, instance):
#         return instance.name.upper()


class OrderProductSerializer(serializers.ModelSerializer):
    product_display = serializers.StringRelatedField(read_only=True, source='product')
    product_url = serializers.HyperlinkedRelatedField(read_only=True, source='product',
                                                      view_name='api_v2:product-detail')
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='api_v2:orderproduct-detail')

    class Meta:
        model = OrderProduct
        fields = ('id', 'url', 'order', 'product', 'amount', 'product_display', 'product_url')


class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    products = OrderProductSerializer(many=True, read_only=True, source='order_products')

    class Meta:
        model = Order
        fields = ('id', 'user', 'first_name', 'last_name', 'phone', 'email',
                  'products', 'status', 'created_at', 'updated_at')


class PasswordValidator:
    def __init__(self, length):
        self.length = length

    def __call__(self, value):
        if len(value) < self.length:
            raise ValidationError(f'Пароль должен быть длинее {self.length} символов')
        return value


def password_validator(value):
    if len(value) < 8:
        raise ValidationError('Пароль должен быть длинее 8 символов')
    return value


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=128, source='password', write_only=True, required=True,
                                             # валидатор в виде функции или объекта класса
                                             validators=[password_validator])

    # валидация всех входящих данных (аналог clean() в формах).
    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают!')
        return super().validate(attrs)

    # валидация для одного поля (password, аналог clean_...() в формах).
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError('Пароль должен быть длинее 8 символов')
        return value

    def create(self, validated_data):
        user = User.objects.create(username=validated_data.get('username'))
        user.set_password(validated_data.get("password"))
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
