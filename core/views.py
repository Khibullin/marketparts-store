from django.shortcuts import render
from catalog.models import Country, Category, Brand


def home(request):
    countries = Country.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')[:8]
    brands = Brand.objects.all().order_by('name')[:8]

    return render(request, 'core/home.html', {
        'countries': countries,
        'categories': categories,
        'brands': brands,
    })