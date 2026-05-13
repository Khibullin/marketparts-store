from django.shortcuts import render, redirect
from catalog.models import Country, Category, Brand


def home(request):
    return redirect('catalog_list')


def guide(request):
    return render(request, 'core/guide.html')


def faq(request):
    return render(request, 'core/faq.html')


def contact(request):
    return render(request, 'core/contact.html')