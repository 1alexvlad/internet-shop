from django.urls import path

from .views import ProductView, ProductDetailView, CatalogView

app_name = 'shop'

urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('catalog/<slug:category_slug>/', CatalogView.as_view(), name='catalog'),
    path('search/', CatalogView.as_view(), name='search'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
