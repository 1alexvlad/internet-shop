from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from .models import Product


class ProductView(TemplateView):
    template_name = 'base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop'
        return context


class CatalogView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self): 
        category_slug = self.kwargs.get('category_slug')
        products = Product.objects.filter(available=True)


        if category_slug and category_slug != 'all':
            products = products.filter(category__slug=category_slug)

        query = self.request.GET.get('q')
        if query:
            products = products.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        sort_by = self.request.GET.get('sort', 'default')
        if sort_by == 'asc':
            products = products.order_by('price')
        elif sort_by == 'desc':
            products = products.order_by('-price')
        else:
            products = products.order_by('id')

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['sort_by'] = self.request.GET.get('sort', 'default')
        context['query'] = self.request.GET.get('q', '')
        context['category_slug'] = self.kwargs.get('category_slug')
        context['show_sort_form'] = True
        return context


class ProductDetailView(DetailView):
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context