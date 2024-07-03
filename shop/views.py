from django.shortcuts import render, get_object_or_404
from .models import Category, ProductProxy

from django.db.models import Q

from django.core.paginator import Paginator


def products_view(request):
    products = ProductProxy.objects.all()
    sort_by = request.GET.get('sort', 'default')

    if sort_by == 'asc':
        products = products.order_by('price')
    elif sort_by == 'desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('id')

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/index.html', {'page_obj': page_obj, 'sort_by': sort_by})



def product_detail(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def search_view(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'default')

    if query:
        products = ProductProxy.objects.filter(
            Q(title__icontains=query))
    else:
        products = ProductProxy.objects.all()

    if sort_by == 'asc':
        products = products.order_by('price')
    elif sort_by == 'desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('id')

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/search.html', {'page_obj': page_obj, 'query': query, 'sort_by': sort_by})

