from django.core.management.base import BaseCommand
from django.db import connection
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        # Очищаем таблицы через TRUNCATE со сбросом ID
        with connection.cursor() as cursor:
            # Получаем системные имена таблиц из моделей Django
            prod_table = Product._meta.db_table
            cat_table = Category._meta.db_table

            # Выполняем TRUNCATE каскадом (сначала продукты, потом категории)
            # RESTART IDENTITY сбрасывает счетчики ID до 1
            cursor.execute(f"TRUNCATE TABLE {prod_table}, {cat_table} RESTART IDENTITY CASCADE;")

        self.stdout.write('Старые данные удалены (таблицы очищены через TRUNCATE).')

        # Создаём категории
        cat1 = Category.objects.create(name='Электроника', description='Гаджеты и техника')
        cat2 = Category.objects.create(name='Одежда', description='Одежда и аксессуары')

        # Создаём продукты
        products = [
            Product(name='Телефон', description='Смартфон', price=29999, category=cat1),
            Product(name='ПК', description='Игровой ПК', price=120999, category=cat1),
            Product(name='Ноутбук', description='Игровой ноутбук', price=89999, category=cat1),
            Product(name='Куртка', description='Зимняя куртка', price=5999, category=cat2),
            Product(name='Кроссовки', description='Спортивные', price=3999, category=cat2),
        ]
        Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS('База успешно заполнена тестовыми данными!'))
