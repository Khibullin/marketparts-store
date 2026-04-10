from django.shortcuts import render, get_object_or_404
from .models import Product


def catalog_list(request):
    products = Product.objects.filter(is_published=True)
    return render(request, 'catalog/catalog_list.html', {
        'products': products
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_published=True)
    return render(request, 'catalog/product_detail.html', {
        'product': product
    })