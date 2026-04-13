from django.contrib import admin
from .models import Country, Brand, CarModel, Category, Product, SellerProfile, ProductImage


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country__name')


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'get_country')
    list_filter = ('brand__country', 'brand')
    search_fields = ('name', 'brand__name', 'brand__country__name')

    def get_country(self, obj):
        return obj.brand.country.name
    get_country.short_description = 'Страна'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'user')
    search_fields = ('name', 'phone', 'user__username')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')
    search_fields = ('product__title', 'product__article')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'article',
        'price',
        'seller_name',
        'brand',
        'car_model',
        'category',
        'condition',
        'status',
        'created_at',
    )
    list_filter = ('status', 'condition', 'brand__country', 'brand', 'category')
    search_fields = ('title', 'article', 'seller_name', 'description', 'compatibility')