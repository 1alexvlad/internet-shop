from django.db import models
from django.urls import reverse



class Category(models.Model):
    name = models.CharField('Категория', max_length=250, unique=True, blank=False, null=False)
    slug = models.SlugField('URL', max_length=250, unique=True, blank=False, null=False)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(("Название"), max_length=250, unique=True, blank=False, null=False, db_index=True)
    description = models.TextField(("Описание"), blank=True)
    slug = models.SlugField(("URL"), max_length=250, unique=True, blank=False, null=False)
    price = models.DecimalField(("Цена"), max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField(("Изображение"), upload_to='products/products/%Y/%m/%d', default='products/products/default/image.png')
    available = models.BooleanField(("Наличие"), default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['price']),
        ]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[str(self.slug)])