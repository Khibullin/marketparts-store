from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Страна')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='brands',
        verbose_name='Страна'
    )
    name = models.CharField(max_length=100, unique=True, verbose_name='Марка')

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='models',
        verbose_name='Марка'
    )
    name = models.CharField(max_length=100, verbose_name='Модель')

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
        ordering = ['brand__name', 'name']
        unique_together = ('brand', 'name')

    def __str__(self):
        return f'{self.brand.name} {self.name}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новая'),
        ('used', 'Б/у'),
    ]

    title = models.CharField(max_length=255, verbose_name='Название товара')
    article = models.CharField(max_length=100, verbose_name='Артикул')
    price = models.PositiveIntegerField(verbose_name='Цена')
    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        default='new',
        verbose_name='Состояние'
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Марка'
    )
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Модель'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Категория'
    )

    seller_name = models.CharField(max_length=255, verbose_name='Название магазина')
    whatsapp_number = models.CharField(max_length=30, verbose_name='WhatsApp')
    compatibility = models.TextField(blank=True, verbose_name='Подходит для')
    description = models.TextField(blank=True, verbose_name='Описание')

    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.article})'