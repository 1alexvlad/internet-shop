from django.urls import path
from .views import products_view, product_detail, search_view

# from . import views 

app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('search/', search_view, name='search'),
    path('<slug:slug>/', product_detail, name='product_detail'),
]