from django.urls import path
from .views import products_view, product_detail, category_list


app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('<slug:slug>/', product_detail, name='product_detail'),
    path('search/<slug:slug>/', category_list, name='category-list'),
]