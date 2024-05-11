import os
import json
from django.core.management.base import BaseCommand
from nxtbn.product.models import Category
from django.conf import settings
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Create categories and subcategories'

    def handle(self, *args, **options):
        json_file_path = os.path.join(settings.BASE_DIR, 'nxtbn', 'seeder_files', 'categories.json')
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            self.create_categories(data['category'])

    def create_categories(self, category_data, parent=None, depth=0):
        category_name = category_data['name']
        category, created = Category.objects.get_or_create(
            name=category_name,
            parent=parent
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Category already exists: {category_name}'))
        
        if depth >= 2:
            return

        for subcategory_data in category_data['subcategories']:
            self.create_categories(subcategory_data, parent=category, depth=depth+1)