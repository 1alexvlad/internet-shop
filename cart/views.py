from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from shop.models import ProductProxy
from .cart import Cart

from django.views import View


class CartView(View):
    template_name = 'cart/cart-view.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        context = {
            'title': 'Корзина'
        }
        return render(request, self.template_name, context)

class CartAddView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        if request.POST.get('action') == 'post':

            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            product = get_object_or_404(ProductProxy, id=product_id)

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