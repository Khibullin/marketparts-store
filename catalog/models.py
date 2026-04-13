from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новая'),
        ('used', 'Б/у'),
    ]

    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('hidden', 'Скрыт'),
        ('sold', 'Продан'),
    ]

    title = models.CharField(max_length=255)
    article = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='new')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    seller_name = models.CharField(max_length=255)
    whatsapp_number = models.CharField(max_length=30)

    main_image = models.ImageField(upload_to='products/', null=True, blank=True)

    compatibility = models.TextField(blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.article})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Фото для {self.product.title}"