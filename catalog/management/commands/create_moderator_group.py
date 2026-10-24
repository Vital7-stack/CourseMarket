from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем все права для модели Product
        ct = ContentType.objects.get_for_model(Product)

        # Находим наше кастомное право
        custom_perm = Permission.objects.get(codename='can_unpublish_product')

        # Добавляем права в группу
        group.permissions.add(custom_perm)

        # Разрешаем удалять любые продукты (стандартное право delete)
        delete_perm = Permission.objects.filter(content_type=ct, codename__startswith='delete').first()
        if delete_perm:
            group.permissions.add(delete_perm)

        self.stdout.write(self.style.SUCCESS(
            f'Группа "Модератор продуктов" {"создана" if created else "уже существует"}. Назначены права.'))