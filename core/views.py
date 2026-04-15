from django.shortcuts import render
from catalog.models import Country, Category, Brand


def home(request):
    countries = Country.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    brands = Brand.objects.all().order_by('name')

    return render(request, 'core/home.html', {
        'countries': countries,
        'categories': categories,
        'brands': brands,
    })


def guide(request):
    return render(request, 'core/guide.html')


def faq(request):
    return render(request, 'core/faq.html')


def contact(request):
    return render(request, 'core/contact.html')