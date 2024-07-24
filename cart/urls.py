from django.urls import path
from .views import CartView, CartAddView, CardDeleteView, CardUpdateView


app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart-view'),
    path('add/', CartAddView.as_view(), name='add-to-cart'),
    path('delete/', CardDeleteView.as_view(), name='delete-to-cart'),
    path('update/', CardUpdateView.as_view(), name='update-to-cart'),
]