from django.contrib.auth.models import User
from django.test import TestCase
from webapp.models import Order, Product


class OrderTest(TestCase):
    def setUp(self):
        p1 = Product.objects.create(name='Test 1', price=10.0)
        p2 = Product.objects.create(name='Test 2', price=20.0)
        p3 = Product.objects.create(name='Test 3', price=30.0)
        self.products = [p1, p2, p3]

    def test_get_total(self):
        order = Order.objects.create(phone='123456')
        order.order_products.create(product=self.products[0], amount=10)
        total = order.get_total()
        self.assertEqual(total, 100, f'Invalid amount, expected: 100, got: {total}')
        order.order_products.create(product=self.products[1], amount=20)
        total = order.get_total()
        self.assertEqual(total, 500, f'Invalid amount, expected: 500, got: {total}')


class ProductAddTest(TestCase):
    def setUp(self):
        admin, created = User.objects.get_or_create(username='admin')
        if created:
            admin.is_superuser = True
            admin.set_password('admin')
            admin.save()
        self.client.login(username='admin', password='admin')

    def test_add_product(self):
        data = {'name': 'CreateTestProduct', 'price': '100', 'category': 'other'}
        response = self.client.post('/products/create/', data=data)
        self.assertEqual(response.status_code, 302)  # редирект после создания товара
        product = Product.objects.filter(name='CreateTestProduct')
        self.assertEqual(len(product), 1)
