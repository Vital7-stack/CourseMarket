from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        # Импортируем модель здесь, а не наверху
        from .models import Product

        @receiver(post_save, sender=Product)
        def clear_product_cache(sender, instance, **kwargs):
            try:
                logger.info(f"Очищаем кэш для продукта {instance.id}")
                cache.delete(f'product_{instance.id}')
                cache.delete(f'category_{instance.category_id}')
            except Exception as e:
                logger.error(f"Ошибка при очистке кэша: {str(e)}")

        @receiver(post_delete, sender=Product)
        def clear_deleted_product_cache(sender, instance, **kwargs):
            try:
                logger.info(f"Очищаем кэш при удалении продукта {instance.id}")
                cache.delete(f'product_{instance.id}')
                cache.delete(f'category_{instance.category_id}')
            except Exception as e:
                logger.error(f"Ошибка при очистке кэша: {str(e)}")