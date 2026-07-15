from django.core.management.base import BaseCommand

from store.models import (
    Category,
    ContactMessage,
    FAQ,
    Feature,
    Order,
    OrderItem,
    Partner,
    Product,
    ProductFeatureConfig,
)


class Command(BaseCommand):
    help = 'Загружает примерные данные в базу'

    def handle(self, *args, **options):
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
                defaults={'name': cat_data['name']},
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Категория: {category.name}'))

        products_data = [
            {
                'name': 'Классическая футболка',
                'slug': 'classic-t-shirt',
                'description': 'Классическая футболка из хлопка.',
                'price': 189000,
                'old_price': 220000,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                'available_sizes': 'S, M, L, XL',
                'available_colors': 'Черный, Белый, Синий',
                'stock': 50,
            },
            {
                'name': 'Джинсы классические',
                'slug': 'classic-jeans',
                'description': 'Классические джинсы из денима.',
                'price': 349000,
                'old_price': None,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                'available_sizes': 'M, L, XL',
                'available_colors': 'Синий, Черный',
                'stock': 30,
            },
            {
                'name': 'Элегантное платье',
                'slug': 'elegant-dress',
                'description': 'Платье для особых случаев.',
                'price': 459000,
                'old_price': None,
                'category': 'womens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400',
                'available_sizes': 'S, M, L',
                'available_colors': 'Черный, Красный',
                'stock': 25,
            },
            {
                'name': 'Демисезонная куртка',
                'slug': 'demiseason-jacket',
                'description': 'Куртка для прохладной погоды.',
                'price': 620000,
                'old_price': 690000,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
                'available_sizes': 'M, L, XL',
                'available_colors': 'Черный, Серый',
                'stock': 20,
            },
            {
                'name': 'Рубашка офисная',
                'slug': 'office-shirt',
                'description': 'Офисная рубашка.',
                'price': 245000,
                'old_price': None,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400',
                'available_sizes': 'S, M, L',
                'available_colors': 'Белый, Голубой',
                'stock': 40,
            },
            {
                'name': 'Свитшот уютный',
                'slug': 'cozy-sweatshirt',
                'description': 'Мягкий свитшот.',
                'price': 275000,
                'old_price': None,
                'category': 'mens-clothing',
                'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400',
                'available_sizes': 'M, L, XL',
                'available_colors': 'Серый, Черный',
                'stock': 35,
            },
        ]

        products = []
        for product_data in products_data:
            category = categories[product_data.pop('category')]
            image_url = product_data.pop('image_url', '')
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'category': category,
                    'rating': 4.5,
                    'reviews_count': 12,
                    'image_url': image_url,
                    'is_active': True,
                },
            )
            if not created and product.price < 1000:
                product.price = product_data['price']
                product.old_price = product_data.get('old_price')
                product.save(update_fields=['price', 'old_price'])
            products.append(product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Товар: {product.name}'))

        for feature_data in [
            {'icon': 'fas fa-shipping-fast', 'title': 'Быстрая доставка', 'description': '2–5 дней', 'order': 0},
            {'icon': 'fas fa-undo', 'title': 'Лёгкий возврат', 'description': '14 дней', 'order': 1},
            {'icon': 'fas fa-shield-alt', 'title': 'Гарантия качества', 'description': 'Проверенные товары', 'order': 2},
        ]:
            Feature.objects.get_or_create(
                title=feature_data['title'],
                defaults={**feature_data, 'is_active': True},
            )

        if not ProductFeatureConfig.objects.exists():
            ProductFeatureConfig.objects.create(
                title='Бесплатная доставка',
                icon='fas fa-shipping-fast',
                text='От 300 000 сум',
                order=1,
                is_active=True,
            )

        for p in [
            {'name': 'Click', 'icon': 'fas fa-credit-card', 'order': 0},
            {'name': 'Payme', 'icon': 'fas fa-wallet', 'order': 1},
            {'name': 'UzPost', 'icon': 'fas fa-truck', 'order': 2},
        ]:
            Partner.objects.get_or_create(name=p['name'], defaults={**p, 'is_active': True})

        for i, (q, a) in enumerate([
            ('Как оформить заказ?', 'Добавьте товары в корзину и оформите заказ.'),
            ('Сроки доставки?', 'Ташкент 1–2 дня, регионы 2–5 дней.'),
            ('Можно вернуть товар?', 'Да, в течение 14 дней.'),
        ]):
            FAQ.objects.get_or_create(
                question=q,
                defaults={'answer': a, 'order': i, 'is_active': True},
            )

        if not ContactMessage.objects.exists():
            ContactMessage.objects.create(
                name='Дилшод',
                email='dilshod@example.com',
                phone='+998901112233',
                subject='delivery',
                message='Есть доставка в Самарканд?',
                is_read=False,
            )
            ContactMessage.objects.create(
                name='Малика',
                email='malika@example.com',
                phone='+998907778899',
                subject='product',
                message='Платье есть в размере S?',
                is_read=False,
            )
            self.stdout.write(self.style.SUCCESS('Сообщения созданы'))

        if not Order.objects.exists() and len(products) >= 6:
            demos = [
                ('Алишер', 'Каримов', 'pending', 'card', [(0, 2, 'M', 'Черный')]),
                ('Нигора', 'Рахимова', 'processing', 'cash', [(2, 1, 'S', 'Черный')]),
                ('Жавлон', 'Усманов', 'delivered', 'wallet', [(1, 1, 'L', 'Синий'), (4, 1, 'M', 'Белый')]),
                ('Сара', 'Исмоилова', 'cancelled', 'card', [(5, 1, 'L', 'Серый')]),
            ]
            for first, last, status, pay, items in demos:
                lines = []
                total = 0
                for idx, qty, size, color in items:
                    product = products[idx]
                    lines.append((product, qty, size, color))
                    total += product.price * qty
                order = Order.objects.create(
                    session_key='demo-seed',
                    first_name=first,
                    last_name=last,
                    email=f'{first.lower()}@example.com',
                    phone='+998901234567',
                    address='ул. Навои, 12',
                    city='Ташкент',
                    total=total,
                    status=status,
                    payment_method=pay,
                )
                for product, qty, size, color in lines:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=qty,
                        price=product.price,
                        size=size,
                        color=color,
                    )
                self.stdout.write(self.style.SUCCESS(f'Заказ #{order.id} ({status})'))

        self.stdout.write(self.style.SUCCESS('Тестовые данные готовы.'))
