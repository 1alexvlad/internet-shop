from django.test import TestCase
from ..forms import ShippingAddressForm
from ..models import ShippingAddress
from django.contrib.auth import get_user_model


User = get_user_model()


class ShippingAddressFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user( username='testuser', password='sdfkjFKJLAFJ4230409')

    def test_valid_form(self):
        """Проверяем, что форма валидна с корректными данными"""
        form_data = {
            'full_name': 'Ivan Ivanov Ivanovich',
            'email': "test_ivan@mail.com", 
            'street_address': 'Lomonosova', 
            'apartment_address': 'Apartement 11'
        }
        form = ShippingAddressForm(data=form_data)
        self.assertTrue(form.is_valid())
        shipping_address = form.save(commit=False)
        shipping_address.user = self.user
        shipping_address.save()
        self.assertEqual(ShippingAddress.objects.count(), 1)

    def test_invalid_form_empty_fields(self):
        """Проверяем, что форма не валидна с пустыми обязательными полями"""
        form_data = {
            'full_name': '',
            'email': 'test_ivan@example.com',
            'street_address': '',
            'apartment_address': 'Apartement 11'
        }
        form = ShippingAddressForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertIn('street_address', form.errors)

    def test_invali_form_email(self):
        """Проверяем, что форма не валидна с некорректным email"""
        form_data = {
            'full_name': 'Ivan Ivanov Ivanovich',
            'email': "test_ivanmail.com", 
            'street_address': 'Lomonosova', 
            'apartment_address': 'Apartement 11'
        }        
        form = ShippingAddressForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)