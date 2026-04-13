from django import forms

from .models import SellerProfile, Product, Country, Brand, CarModel


class SellerRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    class Meta:
        model = SellerProfile
        fields = ['name', 'phone']
        labels = {
            'name': 'Название магазина',
            'phone': 'Телефон / WhatsApp',
        }


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['name', 'phone']
        labels = {
            'name': 'Название магазина',
            'phone': 'Телефон / WhatsApp',
        }


class ProductForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all().order_by('name'),
        required=False,
        label='Страна'
    )

    class Meta:
        model = Product
        fields = [
            'country',
            'brand',
            'car_model',
            'category',
            'title',
            'article',
            'price',
            'condition',
            'status',
            'main_image',
            'compatibility',
            'description',
        ]
        labels = {
            'country': 'Страна',
            'brand': 'Марка',
            'car_model': 'Модель',
            'category': 'Категория',
            'title': 'Название товара',
            'article': 'Артикул',
            'price': 'Цена',
            'condition': 'Состояние',
            'status': 'Статус',
            'main_image': 'Главное фото',
            'compatibility': 'Подходит для',
            'description': 'Описание',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['brand'].queryset = Brand.objects.none()
        self.fields['car_model'].queryset = CarModel.objects.none()

        country_id = None
        brand_id = None

        if self.data.get('country'):
            country_id = self.data.get('country')
        elif self.initial.get('country'):
            country_id = self.initial.get('country')
        elif self.instance.pk and self.instance.brand:
            country_id = self.instance.brand.country_id

        if country_id:
            self.fields['brand'].queryset = Brand.objects.filter(
                country_id=country_id
            ).order_by('name')

        if self.data.get('brand'):
            brand_id = self.data.get('brand')
        elif self.initial.get('brand'):
            brand_id = self.initial.get('brand')
        elif self.instance.pk and self.instance.brand:
            brand_id = self.instance.brand_id

        if brand_id:
            self.fields['car_model'].queryset = CarModel.objects.filter(
                brand_id=brand_id
            ).order_by('name')