from django.test import TestCase
from ..models import ShippingAddress
from ..forms import ShippingAddressForm
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

User = get_user_model()


class ShippingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='sdfkjFKJLAFJ4230409')
        
        self.client.login(username='testuser', password='sdfkjFKJLAFJ4230409')

    def test_shipping_view_success(self):
        """Проверяем, что ShippingView возвращает статус 200 для авторизованного пользователя"""
        response = self.client.get(reverse('payment:shipping'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shipping/shipping.html')

    def test_shipping_view_get_unauthenticated(self):
        """Проверяем, что неавторизованный пользователь перенаправляется на страницу входа"""
        self.client.logout()
        response = self.client.get(reverse('payment:shipping'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/?next=/payment/shipping/')

    def test_shipping_view_post_success(self):
        """Ожидаем, что форма будет валидна """
        data = {
            'full_name': 'Ivan ivanov',
            'email': 'test@example.com',
            'street_address': '123 Main St',
            'apartment_address': '4'
        }
        response = self.client.post(reverse('payment:shipping'), data)
        self.assertRedirects(response, reverse('account:dashboard'))

    def test_shippint_view_post_invalid(self):
        """Ожидаем, что форма будет содержать ошибки при отправке некорректных данных"""
        data = {
            'full_name': '',
            'email': 'test@example.com',
            'street_address': '',
            'apartment_address': '4'
        }
        response = self.client.post(reverse('payment:shipping'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shipping/shipping.html')
        self.assertIsInstance(response.context['form'], ShippingAddressForm)
        self.assertTrue(response.context['form'].errors)


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='sdfkjFKJLAFJ4230409')

        self.shipping_address = ShippingAddress.objects.create(full_name = 'Ivan Ivanov Ivanovich', email="test_ivan@mail.com", street_address='Lomonosova', apartment_address=1, user=self.user)

    def test_checkout_view_success(self):
        """Проверяем, что CheckoutView возвращает статус 200 для авторизованного пользователя"""
        self.client.login(username='testuser', password='sdfkjFKJLAFJ4230409')
        response = self.client.get(reverse('payment:checkout'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/checkout.html')
        self.assertEqual(response.context['shipping_address'], self.shipping_address)

    def test_checkout_view_unauthenticated(self):
        """Проверяем, что неавторизованный пользователь перенаправляется на страницу входа"""
        response = self.client.get(reverse('payment:checkout'))
        self.assertRedirects(response, '/account/login/?next=/payment/checkout/')
        self.assertEqual(response.status_code, 302)
    

class PaymentSuccessViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpa234ЫВАЫВАord'
        )
        self.client.login(username='testuser', password='testpa234ЫВАЫВАord')  # Логиним пользователя

    def test_payment_success_view_with_session_key(self):
        self.client.session['session_key'] = 'some_value'
        response = self.client.get(reverse('payment:payment-success'))

        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'payment/payment-success.html')


class PaymentFailedViewTest(TestCase):
    
    def test_status_code(self):
        """Проверка, что страница доступна и возрвщает статус 200"""
        response = self.client.get(reverse('payment:payment-failed'))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        """Проверка, что используется правильный шаблог"""
        response = self.client.get(reverse('payment:payment-failed'))
        self.assertTemplateUsed(response, 'payment/payment-failed.html')
