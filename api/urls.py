from django.urls import path, include, re_path

from .views import *

app_name = 'api'


urlpatterns = [
    path('product/', ProductList.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),

    path('user/', UserList.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
]
