from django.urls import path
from .views import products_view, product_detail, search_view, catalog_view 

# from . import views 

app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('catalog/<slug:category_slug>', catalog_view, name='catalog'),
    path('search/', search_view, name='search'),
    # path('<category/slug:slug>/', category, name='category'),
    path('<slug:slug>/', product_detail, name='product_detail'),
]