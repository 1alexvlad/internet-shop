from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from shop.models import Product
from .cart import Cart
from .models import PromoCode

from django.views import View


class CartView(View):
    template_name = 'cart/cart-view.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        promo_code = request.GET.get('promo_code', '')
        discount = 0
        error_message = ''

        # Проверяем, есть ли введенный промокод
        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code, is_active=True)
                discount = promo.discount_percent
            except PromoCode.DoesNotExist:
                # Промокод не найден или неактивен
                error_message = 'Промокод недействителен.'

        total_price = cart.get_total_price()
        discounted_price = total_price * (1 - discount / 100) if discount > 0 else total_price

        context = {
            'title': 'Корзина',
            'cart': cart,
            'discount': discount,
            'discounted_price': discounted_price,
            'promo_code': promo_code,
            'error_message': error_message,
        }
        return render(request, self.template_name, context)

class CartAddView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        if request.POST.get('action') == 'post':

            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            product = get_object_or_404(Product, id=product_id)

            cart.add(product=product, quantity=product_qty)
            cart_qty = cart.__len__()

            response = JsonResponse({'qty': cart_qty, "product":product.title})

            return response


class CardDeleteView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            cart.delete(product=product_id)

            cart_qty = cart.__len__()
            cart_total = cart.get_total_price()

            response = JsonResponse({'qty': cart_qty, 'total': cart_total})

            return response


class CardUpdateView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))

            cart.update(product=product_id, quantity=product_qty)

            cart_qty = cart.__len__()
            cart_total = cart.get_total_price()

            response = JsonResponse({'qty': cart_qty, 'total': cart_total})

            return response