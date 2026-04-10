from django.core.management.base import BaseCommand
from catalog.models import Brand, CarModel, Category, Product


class Command(BaseCommand):
    help = 'Заполнение тестовыми товарами'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()

        hyundai = Brand.objects.get(name='Hyundai')
        kia = Brand.objects.get(name='Kia')
        toyota = Brand.objects.get(name='Toyota')
        bmw = Brand.objects.get(name='BMW')

        tucson = CarModel.objects.get(name='Tucson', brand=hyundai)
        sportage = CarModel.objects.get(name='Sportage', brand=kia)
        camry = CarModel.objects.get(name='Camry', brand=toyota)
        x5 = CarModel.objects.get(name='X5', brand=bmw)

        engine = Category.objects.get(name='Двигатель')
        suspension = Category.objects.get(name='Подвеска')
        brakes = Category.objects.get(name='Тормоза')
        filters = Category.objects.get(name='Фильтры')

        Product.objects.create(
            title='Свеча зажигания AG Parts',
            article='D20T0120700',
            price=12000,
            condition='new',
            brand=hyundai,
            car_model=tucson,
            category=engine,
            seller_name='AG Parts Store',
            whatsapp_number='77771234567',
            compatibility='Hyundai Tucson, Kia Sportage',
            description='Оригинальная свеча зажигания, новая, в наличии.',
            is_published=True,
        )

        Product.objects.create(
            title='Свечи комплект 4 шт',
            article='D20T0120700-K4',
            price=15500,
            condition='new',
            brand=hyundai,
            car_model=tucson,
            category=engine,
            seller_name='AG Parts Store',
            whatsapp_number='77771234567',
            compatibility='Hyundai Tucson, Kia Sportage',
            description='Комплект свечей зажигания 4 шт.',
            is_published=True,
        )

        Product.objects.create(
            title='Амортизатор передний',
            article='AMR-12345',
            price=25000,
            condition='used',
            brand=toyota,
            car_model=camry,
            category=suspension,
            seller_name='Japan Parts',
            whatsapp_number='77775554433',
            compatibility='Toyota Camry 40, Toyota Camry 50',
            description='Передний амортизатор, хорошее состояние.',
            is_published=True,
        )

        Product.objects.create(
            title='Тормозные колодки',
            article='BRK-67890',
            price=8000,
            condition='new',
            brand=kia,
            car_model=sportage,
            category=brakes,
            seller_name='Korea Parts',
            whatsapp_number='77779998877',
            compatibility='Kia Sportage, Hyundai Tucson',
            description='Новые тормозные колодки, комплект.',
            is_published=True,
        )

        Product.objects.create(
            title='Масляный фильтр',
            article='FLT-10001',
            price=4500,
            condition='new',
            brand=bmw,
            car_model=x5,
            category=filters,
            seller_name='Euro Parts',
            whatsapp_number='77770001122',
            compatibility='BMW X5, BMW X6',
            description='Масляный фильтр, новый.',
            is_published=True,
        )

        self.stdout.write(self.style.SUCCESS('Тестовые товары успешно загружены!'))