from django.utils import timezone
from django.urls import reverse
from ..models import Category, Product
from django.test import TestCase

from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile


class CategoryTest(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(name='Category 1', slug='category-1')

    def test_unique_name_and_slug(self):
        """Проверяем, что будет ошибка если будут неуникальные поля slug и name"""
        # Используем atomic для обработки исключений
        try:
            with transaction.atomic():
                Category.objects.create(name='Category 1', slug='category-1')  # Не уникальное имя и slug
                Category.objects.create(name='Category 1', slug='category-2')  # Не уникальное имя
                Category.objects.create(name='Category 2', slug='category-1')  # Не уникальный slug
        except IntegrityError:
            pass

        # Проверяем, что категории созданы успешно
        self.assertEqual(Category.objects.count(), 1)

    def test_created_field(self):
        """Проверяем, что поле created устанавливается автоматически"""
        now = timezone.now()
        self.assertIsNotNone(self.category1.created)

        # Проверяем, что created находится в пределах 1 секунды от текущего времени
        self.assertTrue((self.category1.created - now).total_seconds() < 1)

    def test_str_method(self):
        """Проверяем, что поле name возвращает строку"""
        self.assertIsInstance(self.category1.__str__(), str)



class ProductTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='accessories', slug = 'accessories')

        self.product1 = Product.objects.create(category=self.category, title='scarf', description='', slug='scarf', price=1100, available=True)

    def test_unique_title_and_slug(self):
        """Проверяем, что будет ошибка если будут неуникальные поля title и slug"""
        try:
            with transaction.atomic():
                Product.objects.create(category=self.category, title='scarf', description='', slug='scarf', price=1100, available=True)
                Product.objects.create(category=self.category, title='scarf', description='', slug='asif', price=1100, available=True)
                Product.objects.create(category=self.category, title='name', description='', slug='scarf', price=1100, available=True)
        except IntegrityError:
            pass

        # Проверяем, что категории созданы успешно
        self.assertEqual(Category.objects.count(), 1)
        

    def test_missing_category(self):
        """Проверка обязательного поля category"""
        product = Product(title="Продукт без категории", slug="slug-test")
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_missing_title(self):
        """Проверка обязательного поля title"""
        product = Product.objects.create(category=self.category, slug='absent-title')
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_missing_slug(self):
        """Проверка обязательного поля slug"""
        product = Product.objects.create(category=self.category, title="Продукт без slug")
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_image(self):
        """Проверяем поле image"""
        image_data = b'fake image data'
        image_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')

        product = Product.objects.create(
            category=self.category,
            title="Тестовый продукт",
            slug="test-product",
            image=image_file
        )

        self.assertTrue(product.image)
        self.assertTrue(product.image.name.startswith('products/products/') and 'test_image' in product.image.name)

    def test_created_at_field(self):
        """Проверяем, что created_at установлено при создании"""
        now = timezone.now()
        self.assertIsNotNone(self.product1.created_at)

        self.assertTrue((self.product1.created_at - now).total_seconds() < 1)

    def test_updated_at_on_creation(self):
        """Проверяем, что поле updated_at установлено при создании"""
        self.assertIsNotNone(self.product1.updated_at)
    
    def test_updated_at_on_update(self):
        "Проверяем, что поле updated_at меняется при изменении продукта"
        original_updated_at = self.product1.updated_at

        self.product1.title = 'Новая строка'
        self.product1.save()

        self.assertEqual(self.product1.title, 'Новая строка')
        self.assertNotEqual(original_updated_at, self.product1.updated_at)
        self.assertLess(original_updated_at, self.product1.updated_at)


    def test_str_method(self):
        """Проверяем, что поле title возвращает строку"""
        self.assertIsInstance(self.product1.__str__(), str)

    def test_get_absolute_url(self):
        """Проверяем метод get_absolut_url"""
        product = Product.objects.create(
            category=self.category,
            title="Тестовый продукт",
            slug="test-product",
            price=100.00
        )
        # Ожидаемое значение URL
        expected_url = reverse("shop:product_detail", args=[product.slug])
        
        # Проверяем, что метод get_absolute_url возвращает правильный URL
        self.assertEqual(product.get_absolute_url(), expected_url)