from django.shortcuts import render, get_object_or_404
from .models import Category, ProductProxy, Product
from django.views.generic import ListView

from django.db.models import Q


def products_view(request):
    products = ProductProxy.objects.all()        
    return render(request, 'shop/products.html', {'products': products}) 


def product_detail(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def search_view(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query))
    else:
        products = ProductProxy.objects.none()
    return render(request, 'shop/products.html', {'products': products})

