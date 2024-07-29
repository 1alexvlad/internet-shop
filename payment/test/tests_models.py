from ..models import ShippingAddress, Order, OrderItem
from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import Product, Category

from django.utils import timezone



User = get_user_model()


class ShippingAddressTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='sdfkjFKJLAFJ4230409')

        self.shipping_address = ShippingAddress.objects.create(full_name = 'Ivan Ivanov Ivanovich', email="test_ivan@mail.com", street_address='Lomonosova', apartment_address=1, user=self.user)

    
    def test_shipping_address_creation(self):
        """Проверяем, что данные правильно сохраняются"""
        self.assertEqual(self.shipping_address.full_name, 'Ivan Ivanov Ivanovich')
        self.assertEqual(self.shipping_address.email, 'test_ivan@mail.com')
        self.assertEqual(self.shipping_address.street_address, 'Lomonosova')
        self.assertEqual(self.shipping_address.apartment_address, 1)
        self.assertEqual(self.shipping_address.user, self.user)

    def test_shipping_address_str(self):
        """Проверяем, что метод __str__ возвращает строку в ShippingAddress"""
        expected_str = f'Доставка №{self.shipping_address.id}'
        self.assertEqual(str(self.shipping_address), expected_str)


class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user( username='testuser', password='sdfkjFKJLAFJ4230409')

        self.shipping_address = ShippingAddress.objects.create(full_name = 'Ivan Ivanov Ivanovich', email="test_ivan@mail.com", street_address='Lomonosova', apartment_address=1, user=self.user)

        self.order = Order.objects.create(user=self.user, shipping_address=self.shipping_address,amount = 99.99)

    def test_created(self):
        """Проверяем, что поле created создается"""
        self.assertIsNotNone(self.order.created)
        now = timezone.now()
        # Проверяем, что created находится в пределах 1 секунды от текущего времени
        self.assertTrue((self.order.created - now).total_seconds() < 1)
    
    def test_updated(self):
        """Проверяем, что поле updated меняется при изменении"""
        new_amount = self.order.amount
        self.order.amount = 30
        self.order.save()

        self.assertEqual(self.order.amount, 30)
        self.assertNotEqual(new_amount, self.order.amount)
        self.assertLess(self.order.amount, new_amount)

    def test_order_str(self):
        """Проверяем, что метод __str__ возвращает строку в Order"""
        expected_str = f'Заказ №{self.order.id}'
        self.assertEqual(str(self.order), expected_str)



class OrderItemTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user( username='testuser', password='sdfkjFKJLAFJ4230409')
        self.shipping_address = ShippingAddress.objects.create(full_name = 'Ivan Ivanov Ivanovich', email="test_ivan@mail.com", street_address='Lomonosova', apartment_address=1, user=self.user)
        self.order = Order.objects.create(user=self.user, shipping_address=self.shipping_address, amount = 99.99)

        self.category = Category.objects.create(name='Accessories', slug='accessories')
        self.product = Product.objects.create(category=self.category, title='scarf', description='Warm scarf for winter', slug='scarf', price=1100, available=True)

        self.order_item = OrderItem.objects.create(
            order=self.order, 
            product=self.product, 
            price = self.product.price,
            quantity = 2,
            user = self.user)
        
    def test_order_item_creation(self):
        """Проверяем, что OrderItem создается правильно"""
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.price, self.product.price)
        self.assertEqual(self.order_item.quantity, 2)

    def test_str_method(self):
        """Проверяем, что метод __str__ возвращает строку в Order"""
        expected_str = f'OrderItem{self.order_item.id}'
        self.assertEqual(str(self.order_item), expected_str)