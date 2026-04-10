from django.contrib import admin
from .models import Country, Brand, CarModel, Category, Product


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
        'is_published',
        'created_at',
    )
    list_filter = ('is_published', 'condition', 'brand__country', 'brand', 'category')
    search_fields = ('title', 'article', 'seller_name', 'description', 'compatibility')