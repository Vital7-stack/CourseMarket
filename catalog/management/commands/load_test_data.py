import json                        # не обязателен для этой версии, но можно оставить
from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category

class Command(BaseCommand):
    # Это описание команды: видно, если запустить python manage.py help load_test_data
    help = 'Загружает тестовые продукты и категории, предварительно очистив старые данные'

    def handle(self, *args, **kwargs):
        # 1. Очищаем существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Старые данные удалены'))

        # 2. Загружаем фикстуры
        call_command('loaddata', 'categories.json')
        call_command('loaddata', 'products.json')
        self.stdout.write(self.style.SUCCESS('Тестовые данные загружены из фикстур'))