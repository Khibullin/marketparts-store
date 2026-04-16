from django import forms

from .models import SellerProfile, Product, Country, Brand, CarModel


class SellerRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    class Meta:
        model = SellerProfile
        fields = ['name', 'phone', 'city']
        labels = {
            'name': 'Название магазина',
            'phone': 'Телефон / WhatsApp',
            'city': 'Город',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Например: Auto Parts Алматы'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Например: 77713607040'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Например: Алматы'
            }),
        }


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['name', 'phone', 'city']
        labels = {
            'name': 'Название магазина',
            'phone': 'Телефон / WhatsApp',
            'city': 'Город',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Например: Auto Parts Алматы'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Например: 77713607040'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Например: Алматы'
            }),
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
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Например: Амортизатор передний Camry 40'
            }),
            'article': forms.TextInput(attrs={
                'placeholder': 'Если есть артикул — укажите'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Цена в тенге'
            }),
            'compatibility': forms.Textarea(attrs={
                'placeholder': 'Например: Toyota Camry 40, 2006–2011',
                'rows': 3
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Опишите состояние, оригинал или аналог, комплектность',
                'rows': 5
            }),
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