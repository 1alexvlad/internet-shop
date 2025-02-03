from django.urls import path, include, re_path

from .views import *

app_name = 'api'


urlpatterns = [
    path('product/', ProductList.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product-detail'),

    path('user/', UserList.as_view(), name='users-list'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user-detail'),

    path('category/', CategoryList.as_view(), name='category-list'),
    path('category/<str:slug>/', CategoryProduct.as_view(), name='category-slug'),
]
