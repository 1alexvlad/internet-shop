from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import translation

from shop.models import Category, Product

User = get_user_model()


class ProductTests(APITestCase):
    def setUp(self):
        translation.activate('ru')
        self.category = Category.objects.create(name='Test Name', slug='test-slug', sort_order=1)
        self.product1 = Product.objects.create(category=self.category, title='Test Product_1', description='Test Description', slug='test-product-1', price=1500.00)
        self.product2 = Product.objects.create(category=self.category, title='Test Product_2', description='Test Description', slug='test-product-2', price=800.00)

    
    def test_get_all_products(self):
        url = reverse('api:product-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_products_by_price(self):
        url = reverse('api:product-list')
        response = self.client.get(url, {'price': 800})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.product2.title)
    
    def test_filter_products_by_price_min_price_max_price(self):
        url = reverse('api:product-list')
        response = self.client.get(url, {'min_price': 1000, 'max_price': 2000})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.product1.title)

    def test_search_products_by_title(self):
        url = reverse('api:product-list')
        response = self.client.get(url, {'search': 'Product_1'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.product1.title)



class UserTests(APITestCase):
    def setUp(self):
        translation.activate('ru')
        self.user1 = User.objects.create_user(username='test_user_1', email='test1@gmail.com', password='test_password_1')
        self.user2 = User.objects.create_user(username='test_user_2', email='test2@gmail.com', password='test_password_2')
    

    def test_get_users_all(self):
        url = reverse('api:users-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_user_detail(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:user-detail', args=[self.user1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user1.username)
        self.assertEqual(response.data['email'], self.user1.email)

    def test_update_user(self):
        url = reverse('api:user-detail', args=[self.user1.id])
        self.client.force_authenticate(user=self.user1)  

        data = {self.user1.username: 'updated_username', self.user1.email: 'updated@example.com'}

        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updated_username')       
        self.assertEqual(self.user1.email, 'updated@example.com')       

    def test_update_user_not_owner(self):
        url = reverse('api:user-detail', args=[self.user1.id])
        self.client.force_authenticate(user=self.user2)
        data = {'username': 'updated_username', 'email': 'updated@example.com'}
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  