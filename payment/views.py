from django.conf import settings
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.base import TemplateView

from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress

from yookassa import Configuration, Payment
from cart.cart import Cart


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class ShippingView(LoginRequiredMixin, View):
    template_name = 'shipping/shipping.html'
    login_url = 'account:login'

    def get(self, request, *args, **kwargs):
        # Получаем адрес доставки пользователя или создаем новый
        shipping_address = ShippingAddress.objects.filter(user=request.user).first()
        form = ShippingAddressForm(instance=shipping_address)
        
        context = {
            'form': form,
            'title': 'Доставка'
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Обрабатываем форму при отправке POST-запроса
        shipping_address = ShippingAddress.objects.filter(user=request.user).first()
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('account:dashboard')  # Перенаправление после успешного сохранения

        context = {
            'form': form,
            'title': 'Доставка'
        }
        return render(request, self.template_name, context)


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'payment/checkout.html'
    login_url = 'account:login'

    def get(self, request, *args, **kwargs):
        shipping_address = get_object_or_404(ShippingAddress, user=request.user)
        context = {
            'shipping_address': shipping_address
        }
        return render(request, self.template_name, context)


class CompleteOrderView(View):
    def post(self, request, *args, **kwargs):
        # Получаем данные из POST-запроса
        payment_type = request.POST.get('yookassa-payment')
        name = request.POST.get('name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')

        # Получаем корзину и общую сумму заказа
        cart = Cart(request)
        total_price = cart.get_total_price()

        # Обработка платежа через YooKassa
        if payment_type == "yookassa-payment":
            idempotence_key = uuid.uuid4()
            currency = 'RUB'
            description = 'Товары в корзине'
            payment = Payment.create({
                "amount": {
                    "value": str(total_price * 1),
                    "currency": currency
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": request.build_absolute_uri(reverse('payment:payment-success')),
                },
                "capture": True,
                "test": True,
                "description": description,
            }, idempotence_key)

            # Создание или получение адреса доставки
            shipping_address, _ = ShippingAddress.objects.get_or_create(
                user=request.user,
                defaults={
                    'name': name,
                    'email': email,
                    'street_address': street_address,
                    'apartment_address': apartment_address
                }
            )

            confirmation_url = payment.confirmation.confirmation_url

            # Создание заказа
            if request.user.is_authenticated:
                order = Order.objects.create(
                    user=request.user, shipping_address=shipping_address, amount=total_price)

                for item in cart:
                    OrderItem.objects.create(
                        order=order, product=item['product'], price=item['price'], quantity=item['qty'], user=request.user)

                # Очищаем корзину и перенаправляем на URL подтверждения платежа
                cart.clear()
                return redirect(confirmation_url)

            else:
                order = Order.objects.create(
                    shipping_address=shipping_address, amount=total_price)

                for item in cart:
                    OrderItem.objects.create(
                        order=order, product=item['product'], price=item['price'], quantity=item['qty'])

                # Очищаем корзину и перенаправляем на URL подтверждения платежа
                cart.clear()
                return redirect(confirmation_url)
        
class PaymentSuccessView(View):
    template_name = 'payment/payment-success.html'

    def get(self, request):
        if 'session_key' in request.session:
            del request.session['session_key']
        
        return render(request, self.template_name)


class PaymentFailedView(TemplateView):
    template_name = 'payment/payment-failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
