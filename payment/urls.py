from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('payment-success/', views.PaymentSuccessView.as_view(), name='payment-success'),
    path('payment-failed/', views.PaymentFailedView.as_view(), name='payment-failed'),
    path('shipping/', views.ShippingView.as_view(), name='shipping'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('complete-order/', views.CompleteOrderView.as_view(), name='complete-order'),
]
