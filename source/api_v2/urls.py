from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, OrderViewSet, OrderProductViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-products', OrderProductViewSet)

app_name = 'api_v2'

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
