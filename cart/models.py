from django.db import models
from shop.models import Product
from django.contrib.auth import get_user_model


User = get_user_model()


class CartQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0
    

class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ("id",)

    objects = CartQueryset().as_manager()

    def products_price(self):
        return round(self.product.price * self.quantity, 2)


    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username} | Товар {self.product.title} | Количество {self.quantity}'
            
        return f'Анонимная корзина | Товар {self.product.title} | Количество {self.quantity}'


class PromoCode(models.Model):
    code = models.CharField(("Промокод"), max_length=20, unique=True)
    discount_percent = models.DecimalField(("Скидка"), max_digits=5, decimal_places=2)
    is_active = models.BooleanField(("Активен"), default=True)

    def __str__(self):
        return self.code