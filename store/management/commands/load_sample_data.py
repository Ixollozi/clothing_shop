from django.core.management.base import BaseCommand
from store.models import Category, Product, ProductImage


class Command(BaseCommand):
    help = 'Загружает примерные данные в базу'

    def handle(self, *args, **options):
        # Создание категорий
        categories_data = [
            {'name': 'Деревянная мебель', 'slug': 'wooden-furniture'},
            {'name': 'Металлические изделия', 'slug': 'metal-products'},
            {'name': 'Столы и стулья', 'slug': 'tables-chairs'},
            {'name': 'Шкафы и комоды', 'slug': 'cabinets-dressers'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана категория: {category.name}'))

        # Создание товаров
        products_data = [
            {
                'name': 'Деревянный обеденный стол',
                'slug': 'wooden-dining-table',
                'description': 'Массивный деревянный обеденный стол из натурального дерева. Прочная конструкция и элегантный дизайн.',
                'price': 450.00,
                'old_price': 550.00,
                'category': 'wooden-furniture',
                'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop',
                'available_sizes': '200x100',
                'available_colors': 'Дуб, Орех, Сосна',
                'stock': 12,
            },
            {
                'name': 'Металлическая стеллажная система',
                'slug': 'metal-shelf-system',
                'description': 'Прочная металлическая стеллажная система для хранения. Устойчивая конструкция из качественного металла.',
                'price': 320.00,
                'old_price': None,
                'category': 'metal-products',
                'image_url': 'https://images.unsplash.com/photo-1551292831-023188e34287?w=400&h=400&fit=crop',
                'available_sizes': '180x40',
                'available_colors': 'Серый, Черный, Белый',
                'stock': 18,
            },
            {
                'name': 'Деревянный шкаф',
                'slug': 'wooden-cabinet',
                'description': 'Просторный деревянный шкаф с качественной фурнитурой. Идеален для хранения одежды и вещей.',
                'price': 680.00,
                'old_price': None,
                'category': 'cabinets-dressers',
                'image_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=400&fit=crop',
                'available_sizes': '200x60',
                'available_colors': 'Дуб, Орех, Вишня',
                'stock': 8,
            },
            {
                'name': 'Металлическая кровать',
                'slug': 'metal-bed',
                'description': 'Стильная металлическая кровать с прочным каркасом. Современный дизайн и долговечность.',
                'price': 550.00,
                'old_price': None,
                'category': 'metal-products',
                'image_url': 'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=400&h=400&fit=crop',
                'available_sizes': '160x200, 180x200',
                'available_colors': 'Черный, Серый, Белый',
                'stock': 15,
            },
            {
                'name': 'Деревянное кресло',
                'slug': 'wooden-chair',
                'description': 'Удобное деревянное кресло с эргономичной спинкой. Изготовлено из массива дерева.',
                'price': 280.00,
                'old_price': None,
                'category': 'tables-chairs',
                'image_url': 'https://images.unsplash.com/photo-1506439773649-6c5e9a6d8b12?w=400&h=400&fit=crop',
                'available_sizes': 'Стандарт',
                'available_colors': 'Дуб, Орех, Сосна',
                'stock': 25,
            },
            {
                'name': 'Металлическая полка',
                'slug': 'metal-rack',
                'description': 'Универсальная металлическая полка для гаража или склада. Высокая прочность и устойчивость.',
                'price': 190.00,
                'old_price': None,
                'category': 'metal-products',
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
                'available_sizes': '150x40',
                'available_colors': 'Серый, Черный',
                'stock': 30,
            },
            {
                'name': 'Деревянный комод',
                'slug': 'wooden-dresser',
                'description': 'Элегантный деревянный комод с выдвижными ящиками. Качественная сборка и стильный дизайн.',
                'price': 520.00,
                'old_price': None,
                'category': 'cabinets-dressers',
                'image_url': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&h=400&fit=crop',
                'available_sizes': '120x50',
                'available_colors': 'Дуб, Орех, Вишня',
                'stock': 10,
            },
            {
                'name': 'Металлическая конструкция',
                'slug': 'metal-structure',
                'description': 'Прочная металлическая конструкция для различных целей. Изготовлена из высококачественного металла.',
                'price': 380.00,
                'old_price': None,
                'category': 'metal-products',
                'image_url': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=400&fit=crop',
                'available_sizes': 'Индивидуально',
                'available_colors': 'Серый, Черный',
                'stock': 5,
            },
        ]

        for product_data in products_data:
            category = categories[product_data.pop('category')]
            image_url = product_data.pop('image_url', '')
            
            # Используем внешние URL изображений для примера
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'category': category,
                    'rating': 4.0,
                    'reviews_count': 12,
                    'image_url': image_url,  # Используем внешний URL
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан товар: {product.name}'))
                # Сохраняем URL изображения в комментарии или отдельном поле
                # В реальном проекте используйте загрузку файлов
            else:
                self.stdout.write(self.style.WARNING(f'Товар уже существует: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))

