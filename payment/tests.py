# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from .models import ShippingAddress

# User = get_user_model()

# class ShippingAddressModelTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='sdfkjFKJLAFJ4230409'
#         )

#     def test_create_shipping_address(self):
#         """Тест создания адреса доставки."""
#         shipping_address = ShippingAddress.objects.create(
#             full_name='John Doe',
#             email='john@example.com',
#             street_address='123 Main St',
#             apartment_address='Apt 456',
#             user=self.user
#         )

#         self.assertEqual(shipping_address.full_name, 'John Doe')
#         self.assertEqual(shipping_address.email, 'john@example.com')
#         self.assertEqual(shipping_address.street_address, '123 Main St')
#         self.assertEqual(shipping_address.apartment_address, 'Apt 456')
#         self.assertEqual(shipping_address.user, self.user)
