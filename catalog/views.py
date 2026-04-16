from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from .forms import SellerRegisterForm, SellerProfileForm, ProductForm
from .models import (
    Product,
    ProductImage,
    Country,
    Brand,
    CarModel,
    Category,
    SellerProfile,
)


def catalog_list(request):
    query = request.GET.get('q', '').strip()
    country_id = request.GET.get('country', '').strip()
    brand_id = request.GET.get('brand', '').strip()
    model_id = request.GET.get('model', '').strip()
    category_id = request.GET.get('category', '').strip()

    countries = Country.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')

    brands = Brand.objects.select_related('country').all().order_by('name')
    models = CarModel.objects.select_related('brand', 'brand__country').all().order_by('name')

    if country_id:
        brands = brands.filter(country_id=country_id)

        if brand_id and not brands.filter(id=brand_id).exists():
            brand_id = ''
            model_id = ''

    if brand_id:
        models = models.filter(brand_id=brand_id)

        if model_id and not models.filter(id=model_id).exists():
            model_id = ''
    else:
        if country_id:
            models = models.none()

    products = Product.objects.filter(status='active').select_related(
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
    product = get_object_or_404(Product, pk=pk, status='active')
    return render(request, 'catalog/product_detail.html', {
        'product': product
    })


def seller_register(request):
    error_message = None

    if request.method == 'POST':
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                error_message = 'Пользователь с таким логином уже существует.'
            else:
                user = User.objects.create_user(username=username, password=password)

                SellerProfile.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    phone=form.cleaned_data['phone'],
                    city=form.cleaned_data.get('city', '')
                )

                return redirect('seller_login')
    else:
        form = SellerRegisterForm()

    return render(request, 'catalog/seller_register.html', {
        'form': form,
        'error_message': error_message,
    })


def seller_login(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('seller_dashboard')
        else:
            error_message = 'Неверный логин или пароль.'

    return render(request, 'catalog/seller_login.html', {
        'error_message': error_message,
    })


def seller_logout(request):
    logout(request)
    return redirect('catalog_list')


@login_required
def seller_dashboard(request):
    seller = get_object_or_404(SellerProfile, user=request.user)
    products = Product.objects.filter(seller_name=seller.name).order_by('-created_at')

    return render(request, 'catalog/seller_dashboard.html', {
        'seller': seller,
        'products': products,
    })


@login_required
def seller_profile(request):
    seller = get_object_or_404(SellerProfile, user=request.user)
    products_count = Product.objects.filter(seller_name=seller.name).count()

    return render(request, 'catalog/seller_profile.html', {
        'seller': seller,
        'products_count': products_count,
    })


@login_required
def seller_profile_edit(request):
    seller = get_object_or_404(SellerProfile, user=request.user)
    old_name = seller.name

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=seller)
        if form.is_valid():
            updated_seller = form.save()

            if old_name != updated_seller.name:
                Product.objects.filter(seller_name=old_name).update(
                    seller_name=updated_seller.name,
                    whatsapp_number=updated_seller.phone,
                    city=updated_seller.city
                )
            else:
                Product.objects.filter(seller_name=updated_seller.name).update(
                    whatsapp_number=updated_seller.phone,
                    city=updated_seller.city
                )

            return redirect('seller_profile')
    else:
        form = SellerProfileForm(instance=seller)

    return render(request, 'catalog/seller_profile_edit.html', {
        'seller': seller,
        'form': form,
    })


@login_required
def seller_profile_delete(request):
    seller = get_object_or_404(SellerProfile, user=request.user)

    if request.method == 'POST':
        user = request.user
        Product.objects.filter(seller_name=seller.name).delete()
        seller.delete()
        user.delete()
        logout(request)
        return redirect('catalog_list')

    return render(request, 'catalog/seller_profile_delete.html', {
        'seller': seller,
    })


@login_required
def add_product(request):
    seller = get_object_or_404(SellerProfile, user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        files = request.FILES.getlist('extra_images')

        if form.is_valid():
            product = form.save(commit=False)
            product.seller_name = seller.name
            product.whatsapp_number = seller.phone
            product.city = seller.city
            product.save()

            for f in files[:4]:
                ProductImage.objects.create(product=product, image=f)

            return redirect('seller_dashboard')
    else:
        form = ProductForm()

    return render(request, 'catalog/add_product.html', {
        'form': form,
        'seller': seller,
        'page_title': 'Добавить товар',
        'submit_text': 'Сохранить товар',
    })


@login_required
def edit_product(request, pk):
    seller = get_object_or_404(SellerProfile, user=request.user)
    product = get_object_or_404(Product, pk=pk, seller_name=seller.name)

    initial = {}
    if product.brand:
        initial['country'] = product.brand.country_id

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, initial=initial)
        files = request.FILES.getlist('extra_images')

        if form.is_valid():
            updated_product = form.save(commit=False)

            if request.POST.get('remove_main_image'):
                if product.main_image:
                    product.main_image.delete(save=False)
                updated_product.main_image = None

            if request.POST.get('remove_extra_images'):
                for img in product.images.all():
                    img.image.delete(save=False)
                    img.delete()

            updated_product.seller_name = seller.name
            updated_product.whatsapp_number = seller.phone
            updated_product.city = seller.city
            updated_product.save()

            if files:
                for img in product.images.all():
                    img.image.delete(save=False)
                    img.delete()

                for f in files[:4]:
                    ProductImage.objects.create(product=updated_product, image=f)

            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product, initial=initial)

    return render(request, 'catalog/add_product.html', {
        'form': form,
        'seller': seller,
        'product': product,
        'page_title': 'Редактировать товар',
        'submit_text': 'Сохранить изменения',
    })


@login_required
def delete_product(request, pk):
    seller = get_object_or_404(SellerProfile, user=request.user)
    product = get_object_or_404(Product, pk=pk, seller_name=seller.name)

    if request.method == 'POST':
        product.delete()
        return redirect('seller_dashboard')

    return render(request, 'catalog/delete_product.html', {
        'seller': seller,
        'product': product,
    })


def load_brands(request):
    country_id = request.GET.get('country')
    brands = Brand.objects.filter(country_id=country_id).order_by('name')

    data = [{'id': b.id, 'name': b.name} for b in brands]
    return JsonResponse(data, safe=False)


def load_models(request):
    brand_id = request.GET.get('brand')
    models = CarModel.objects.filter(brand_id=brand_id).order_by('name')

    data = [{'id': m.id, 'name': m.name} for m in models]
    return JsonResponse(data, safe=False)