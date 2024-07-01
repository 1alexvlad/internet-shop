from django.shortcuts import render, get_object_or_404
from .models import Category, ProductProxy


def products_view(request):
    products = ProductProxy.objects.all()        
    return render(request, 'shop/products.html', {'products': products}) 


def product_detail(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})
