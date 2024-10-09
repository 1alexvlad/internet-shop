from django.urls import path, include
from rest_framework import routers

from .views import *

app_name = 'api'


router = routers.SimpleRouter()
router.register(r'user', UserViewSet)


urlpatterns = [
    path('product/', ProductList.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('', include(router.urls)),
]
