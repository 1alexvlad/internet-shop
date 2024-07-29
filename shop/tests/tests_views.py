from django.test import TestCase
from ..models import Product, Category
from django.urls import reverse



class ProductViewTests(TestCase):
    
    def test_product_view_status_code(self):
        """Проверка, что страница доступна и возрвщает статус 200"""
        response = self.client.get(reverse('shop:products'))    
        self.assertEqual(response.status_code, 200)  

    def test_product_template_used(self):
        """Проверка, что используется правильный шаблог"""
        response = self.client.get(reverse('shop:products'))
        self.assertTemplateUsed(response, 'base.html')  

    def test_product_view_context_data(self):
        """Проверка, что контекст содержит правильные данные"""
        response = self.client.get(reverse('shop:products'))
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Shop')



class CatalogViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        self.product1 = Product.objects.create(category=self.category, title='Product 1', slug='product-1', price=100, available=True)
        self.product2 = Product.objects.create(category=self.category, title='Product 2', slug='product-2', price=200, available=True)
        self.product3 = Product.objects.create(category=self.category, title='Product 3', slug='product-3', price=300, available=False)

    def test_catalog_view_status_code(self):
        """Проверка, что страница доступна и возрвщает статус 200"""
        response = self.client.get(reverse('shop:catalog', args=['tst-category']))
        self.assertEqual(response.status_code, 200)

    def test_catalog_view_templated_used(self):
        """Проверка, что используется правильный шаблон"""
        response = self.client.get(reverse('shop:catalog', args=['test-category']))
        self.assertTemplateUsed(response, 'shop/product_list.html')

    def test_catalog_view_products_in_context(self):
        """Проверяем, что продукты передаются в контесте"""
        response = self.client.get(reverse('shop:catalog', args=['test-category']))
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')
        self.assertNotContains(response, 'Product 3')

    def test_catalog_view_search_query(self):
        """Проверка поиска"""
        response = self.client.get(reverse('shop:catalog', args=['test-category']), {'q': 'Product 1'})
        self.assertContains(response, 'Product 1')
        self.assertNotContains(response, 'Product 2')

    def test_catalog_view_sorting_asc(self):
        """Проверка сортировки по возрастанию цены"""
        response = self.client.get(reverse('shop:catalog', args=['test-category']), {'sort': 'asc'})
        products = list(response.context['products'])
        self.assertEqual(products, [self.product1, self.product2])

    def test_catalog_view_sorting_desc(self):
        """Проверка сортировки по уменьшению цены"""
        response = self.client.get(reverse('shop:catalog', args=['test-category']), {'sort': 'desc'})
        products = list(response.context['products'])
        self.assertEqual(products, [self.product2, self.product1])

    def test_catalog_view_context_data(self):
        """Проверка контекста, передаваемого в шаблон."""
        response = self.client.get(reverse('shop:catalog', args=['test-category']))
        self.assertEqual(response.context['title'], 'Каталог')
        self.assertEqual(response.context['category_slug'], 'test-category')



    def test_search_url(self):
        """Проверка, что url работает и возвращает статус 200"""
        response = self.client.get(reverse('shop:search'))
        self.assertEqual(response.status_code, 200)

    def test_search_template_used(self):
        """Проверка, что используется правильный шаблон"""
        response = self.client.get(reverse('shop:search'))
        self.assertTemplateUsed(response, 'shop/product_list.html')

    def test_catalog_view_context_data(self):
        """Проверка контекста, передаваемого в шаблон."""
        response = self.client.get(reverse('shop:search'))
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Каталог')


class ProductDetailViewTest(TestCase):
    def setUp(self):
        # Создаем тестовую категорию
        self.category = Category.objects.create(name='Accessories', slug='accessories')

        # Создаем тестовый продукт
        self.product = Product.objects.create(
            category=self.category,
            title='Scarf',
            description='Warm scarf for winter',
            slug='scarf',
            price=1100,
            available=True
        )

    def test_product_detail_view(self):
        """Проверяем, что ProductDetailView возвращает правильный продукт"""
        url = reverse('shop:product_detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')

    def test_product_detail_view_with_invalid_slug(self):
        """Проверяем, что ProductDetailView возвращает 404 при неверном slug"""
        url = reverse('shop:product_detail', kwargs={'slug': 'invalid-slug'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_product_detail_view_context_data(self):
        """Проверяем, что ProductDetailView передает правильные данные в контекст"""
        url = reverse('shop:product_detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)

        self.assertEqual(response.context['title'], self.product.title)


