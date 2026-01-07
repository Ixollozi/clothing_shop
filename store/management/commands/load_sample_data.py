from django.core.management.base import BaseCommand
from store.models import Category, Product, ProductImage


class Command(BaseCommand):
    help = 'Загружает примерные данные в базу'

    def handle(self, *args, **options):
        # Создание категорий
        categories_data = [
            {'name': 'Мужская одежда', 'slug': 'mens-clothing'},
            {'name': 'Женская одежда', 'slug': 'womens-clothing'},
            {'name': 'Детская одежда', 'slug': 'kids-clothing'},
            {'name': 'Аксессуары', 'slug': 'accessories'},
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
                'name': 'Классическая футболка',
                'slug': 'classic-t-shirt',
                'description': 'Классическая футболка из высококачественного хлопка. Идеально подходит для повседневной носки.',
                'price': 20.00,
                'old_price': 25.00,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                'available_sizes': 'M',
                'available_colors': 'Черный, Белый, Синий',
                'stock': 50,
            },
            {
                'name': 'Джинсы классические',
                'slug': 'classic-jeans',
                'description': 'Классические джинсы из качественного денима. Удобные и стильные.',
                'price': 35.00,
                'old_price': None,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
                'available_sizes': 'L',
                'available_colors': 'Синий, Черный',
                'stock': 30,
            },
            {
                'name': 'Элегантное платье',
                'slug': 'elegant-dress',
                'description': 'Элегантное платье для особых случаев. Красивая и стильная модель.',
                'price': 50.00,
                'old_price': None,
                'category': 'womens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400',
                'available_sizes': 'M',
                'available_colors': 'Черный, Красный, Синий',
                'stock': 25,
            },
            {
                'name': 'Демисезонная куртка',
                'slug': 'demiseason-jacket',
                'description': 'Демисезонная куртка для прохладной погоды. Стильная и практичная.',
                'price': 60.00,
                'old_price': None,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
                'available_sizes': 'L',
                'available_colors': 'Черный, Серый',
                'stock': 20,
            },
            {
                'name': 'Рубашка офисная',
                'slug': 'office-shirt',
                'description': 'Офисная рубашка из качественной ткани. Идеальна для делового стиля.',
                'price': 25.00,
                'old_price': None,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400',
                'available_sizes': 'M',
                'available_colors': 'Белый, Голубой',
                'stock': 40,
            },
            {
                'name': 'Свитшот уютный',
                'slug': 'cozy-sweatshirt',
                'description': 'Уютный свитшот для комфортной носки. Мягкий и теплый.',
                'price': 40.00,
                'old_price': None,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400',
                'available_sizes': 'L',
                'available_colors': 'Серый, Черный',
                'stock': 35,
            },
            {
                'name': 'Юбка миди',
                'slug': 'midi-skirt',
                'description': 'Стильная юбка миди длины. Подходит для офиса и повседневной носки.',
                'price': 28.00,
                'old_price': None,
                'category': 'womens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=400',
                'available_sizes': 'M',
                'available_colors': 'Черный, Серый',
                'stock': 30,
            },
            {
                'name': 'Брюки классические',
                'slug': 'classic-pants',
                'description': 'Классические брюки для делового стиля. Качественная ткань и отличный крой.',
                'price': 33.00,
                'old_price': None,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400',
                'available_sizes': 'L',
                'available_colors': 'Черный, Серый, Синий',
                'stock': 28,
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

