import os
import django
import json

# Инициализация Django (чтобы работали модели)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core import serializers
from catalog.models import Category, Product

# Дамп категорий
with open('catalog/fixtures/categories.json', 'w', encoding='utf-8') as f:
    data = serializers.serialize('json', Category.objects.all(), indent=2)
    f.write(data)
    print("Categories saved successfully.")

# Дамп товаров
with open('catalog/fixtures/products.json', 'w', encoding='utf-8') as f:
    data = serializers.serialize('json', Product.objects.all(), indent=2)
    f.write(data)
    print("Products saved successfully.")