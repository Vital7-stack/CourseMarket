from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Удаляет старые данные и создаёт тестовые продукты и категории'

    def handle(self, *args, **kwargs):
        # 1. Очищаем существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Старые данные удалены'))

        # 2. Создаём категории
        electronics = Category.objects.create(
            name='Электроника',
            description='Телефоны, ноутбуки и гаджеты'
        )
        books = Category.objects.create(
            name='Книги',
            description='Художественная и учебная литература'
        )
        clothes = Category.objects.create(
            name='Одежда',
            description='Футболки, джинсы и аксессуары'
        )

        # 3. Создаём товары
        Product.objects.create(
            name='Смартфон X',
            description='Мощный смартфон с отличной камерой. Идеально подходит для фото и видео.',
            category=electronics,
            price=45000.00
        )
        Product.objects.create(
            name='Ноутбук Pro',
            description='Производительный ноутбук для работы и игр. Лёгкий корпус, долгая батарея.',
            category=electronics,
            price=120000.00
        )
        Product.objects.create(
            name='Война и мир',
            description='Великий роман Льва Толстого о судьбах людей во время войны 1812 года.',
            category=books,
            price=800.00
        )
        Product.objects.create(
            name='Гарри Поттер',
            description='История о юном волшебнике, который узнал о своём истинном предназначении.',
            category=books,
            price=750.00
        )
        Product.objects.create(
            name='Футболка базовая',
            description='Классическая белая футболка из 100% хлопка. Комфортная и стильная.',
            category=clothes,
            price=1500.00
        )
        Product.objects.create(
            name='Джинсы синие',
            description='Прямые джинсы из плотного денима. Универсальный крой для любого случая.',
            category=clothes,
            price=3500.00
        )

        self.stdout.write(self.style.SUCCESS('Тестовые данные созданы'))
