from django.core.cache import cache
from .models import Product, Category


def get_product_by_id(product_id):
    cache_key = f'product_{product_id}'
    product = cache.get(cache_key)

    if not product:
        print(f"[DEBUG] Product Cache MISS for ID {product_id}. Fetching from DB...")
        try:
            product = Product.objects.get(id=product_id)
            cache.set(cache_key, product, timeout=900)
            print(f"[DEBUG] Product ID {product_id} saved to cache.")
        except Product.DoesNotExist:
            return None
    else:
        print(f"[DEBUG] Product Cache HIT for ID {product_id}.")

    return product


def get_products_by_category(category_id):
    cache_key = f'category_{category_id}_ids'
    product_ids = cache.get(cache_key)

    if not product_ids:
        print(f"[DEBUG] Category Cache MISS for ID {category_id}. Fetching IDs from DB...")

        if not Category.objects.filter(id=category_id).exists():
            return []

        product_ids = list(Product.objects.filter(category_id=category_id).values_list('id', flat=True))
        cache.set(cache_key, product_ids, timeout=3600)
        print(f"[DEBUG] Saved {len(product_ids)} product IDs to cache for category {category_id}.")
    else:
        print(f"[DEBUG] Category Cache HIT for ID {category_id}. Using cached IDs.")

    # Получаем все продукты по сохраненным ID
    products = Product.objects.filter(id__in=product_ids)

    # Сохраняем список продуктов в кэш на случай, если нужно будет использовать их сразу
    cache_key_products = f'category_{category_id}_products'
    cache.set(cache_key_products, list(products), timeout=3600)

    return products