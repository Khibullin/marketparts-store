from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Product, Country, Brand, CarModel, Category


def catalog_list(request):
    query = request.GET.get('q', '').strip()
    country_id = request.GET.get('country', '').strip()
    brand_id = request.GET.get('brand', '').strip()
    model_id = request.GET.get('model', '').strip()
    category_id = request.GET.get('category', '').strip()

    countries = Country.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')

    # Базовые queryset для фильтров
    brands = Brand.objects.select_related('country').all().order_by('name')
    models = CarModel.objects.select_related('brand', 'brand__country').all().order_by('name')

    # Сужаем марки по стране
    if country_id:
        brands = brands.filter(country_id=country_id)

        # Если выбрана марка не из этой страны — сбрасываем её
        if brand_id and not brands.filter(id=brand_id).exists():
            brand_id = ''
            model_id = ''

    # Сужаем модели по марке
    if brand_id:
        models = models.filter(brand_id=brand_id)

        # Если выбрана модель не из этой марки — сбрасываем её
        if model_id and not models.filter(id=model_id).exists():
            model_id = ''
    else:
        # Если марка не выбрана, но страна выбрана — модели не показываем все подряд
        if country_id:
            models = models.none()

    products = Product.objects.filter(is_published=True).select_related(
        'brand',
        'brand__country',
        'car_model',
        'category',
    )

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(article__icontains=query) |
            Q(description__icontains=query) |
            Q(compatibility__icontains=query)
        )

    if country_id:
        products = products.filter(brand__country_id=country_id)

    if brand_id:
        products = products.filter(brand_id=brand_id)

    if model_id:
        products = products.filter(car_model_id=model_id)

    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
        'countries': countries,
        'brands': brands,
        'models': models,
        'categories': categories,
        'query': query,
        'selected_country': country_id,
        'selected_brand': brand_id,
        'selected_model': model_id,
        'selected_category': category_id,
    }
    return render(request, 'catalog/catalog_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_published=True)
    return render(request, 'catalog/product_detail.html', {
        'product': product
    })