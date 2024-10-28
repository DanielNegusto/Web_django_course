from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Load test products from fixture and clear existing data'

    def handle(self, *args, **kwargs):
        # Удаляем существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted existing products and categories.'))

        # Загружаем данные из фикстуры
        call_command('loaddata', 'library_fixture.json')

        self.stdout.write(self.style.SUCCESS('Successfully loaded test products from fixture.'))
