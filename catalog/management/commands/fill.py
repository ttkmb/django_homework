import json
from django.core.management import BaseCommand
from django.db import connection
from catalog.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE catalog_category RESTART IDENTITY CASCADE;")
        Category.objects.all().delete()
        Product.objects.all().delete()
        with open('category.json', 'r') as f:
            data = json.load(f)
            category_data = []
            for item in data:
                category_data.append(Category(**item['fields']))
        Category.objects.bulk_create(category_data)

        with open('products.json', 'r') as f:
            data = json.load(f)
            product_data = []
            for item in data:
                category_id = item['fields']['category']
                item['fields']['category'] = Category.objects.get(id=category_id)
                product_data.append(Product(**item['fields']))
        Product.objects.bulk_create(product_data)

