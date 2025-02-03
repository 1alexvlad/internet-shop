from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from rest_framework import filters 

from shop.models import Product, Category

from .serializers import ProductSerializer, UserSerializer, CategorySerializer, CategoryProductSerializer


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductFilter(rest_framework.FilterSet):
    min_price = rest_framework.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = rest_framework.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 'price']


class ProductList(generics.ListAPIView):
    queryset = Product.objects.select_related('category').all().order_by('id')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    
    search_fields = ['title']
    ordering_fields = ['price']

    
class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True
        return obj == request.user

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryProduct(generics.ListAPIView):
    serializer_class = CategoryProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price']

    def get_queryset(self):
        slug = self.kwargs['slug']
        if slug == 'all':
            return Product.objects.all()
        else:
            category = get_object_or_404(Category, slug=slug)
            return Product.objects.filter(category=category)