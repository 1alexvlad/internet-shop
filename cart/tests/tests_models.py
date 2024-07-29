from ..models import CartQueryset, Cart
from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import Category, Product


User = get_user_model()


class CartTets(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='sdfkjFKJLAFJ4230409')

        cls.category = Category.objects.create(name='Accessories', slug='accessories')

        cls.product = Product.objects.create(category=cls.category, title='scarf', description='Testing...', slug='scarf', price=100, available=True)


    def test_cart_creation(self):
        """Проверяем, что данные правильно сохраняются"""
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.product, self.product)
        self.assertEqual(cart.quantity, 2)
        self.assertIsNone(cart.session_key)
        self.assertIsNotNone(cart.created_timestamp)

    def test_caart_creation_without_user(self):
        cart = Cart.objects.create(product=self.product, quantity=2, session_key='abcd1234')
        self.assertIsNone(cart.user)
        self.assertEqual(cart.product, self.product)
        self.assertEqual(cart.quantity, 2)
        self.assertEqual(cart.session_key, 'abcd1234')


    def test_produts_price(self):
        """Тест, что праивльно считает итоговую сумму - products_price"""
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        self.assertEqual(cart.products_price(), 200)

    def test_str_representation_with_user(self):
        """Проверяем, что метод __str__ возвращает строку в Cart для авторизированного пользователя"""
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        self.assertEqual(str(cart), f'Корзина {self.user.username} | Товар {self.product.title} | Количество 2')

    def test_str_representation_without_user(self):
        """Проверяем, что метод __str__ возвращает строку в Cart для неавторизированного пользователя"""
        cart = Cart.objects.create(product=self.product, quantity=2, session_key='abcd1234')
        self.assertEqual(str(cart), f'Анонимная корзина | Товар {self.product.title} | Количество 2')

    def test_total_price(self):
        """Тест, проверяем правильную выполнение функции total_price"""
        cart1 = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        cart2 = Cart.objects.create(user=self.user, product=self.product, quantity=3)
        carts = Cart.objects.filter(user=self.user)
        self.assertEqual(carts.total_price(), 500)

    def test_total_quantity(self):
        """Тест, проверяем правильную выполнение функции total_quantity"""
        cart1 = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        cart2 = Cart.objects.create(user=self.user, product=self.product, quantity=3)
        carts = Cart.objects.filter(user=self.user)
        self.assertEqual(carts.total_quantity(), 5)

