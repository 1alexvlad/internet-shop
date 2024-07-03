from django.shortcuts import render, get_object_or_404
from .models import Category, ProductProxy

from django.db.models import Q

from django.core.paginator import Paginator


def products_view(request):
    products = ProductProxy.objects.all().order_by('id')  
    
    paginator = Paginator(products, 4)  # Показывать 4 продуктов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)     
    return render(request, 'shop/products.html', {'page_obj': page_obj}) 


def product_detail(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def search_view(request):
    query = request.GET.get('q')
    if query:
        products = ProductProxy.objects.filter(
            Q(title__icontains=query))
    else:
        products = ProductProxy.objects.none()

    paginator = Paginator(products, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/products.html', {'page_obj': page_obj, 'query': query})




