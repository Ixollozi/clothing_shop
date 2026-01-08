from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def get_dummy_products():
    """Возвращает заглушки товаров"""
    return [
        {
            'name': 'Classic T-shirt',
            'slug': 'dummy-tshirt',
            'price': 20,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
            'image': None,
        },
        {
            'name': 'Classic Jeans',
            'slug': 'dummy-jeans',
            'price': 35,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
            'image': None,
        },
        {
            'name': 'Elegant Dress',
            'slug': 'dummy-dress',
            'price': 50,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400',
            'image': None,
        },
        {
            'name': 'Demiseason Jacket',
            'slug': 'dummy-jacket',
            'price': 60,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
            'image': None,
        },
        {
            'name': 'Office Shirt',
            'slug': 'dummy-shirt',
            'price': 25,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400',
            'image': None,
        },
        {
            'name': 'Cozy Sweatshirt',
            'slug': 'dummy-sweatshirt',
            'price': 40,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400',
            'image': None,
        },
        {
            'name': 'Midi Skirt',
            'slug': 'dummy-skirt',
            'price': 28,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=400',
            'image': None,
        },
        {
            'name': 'Classic Pants',
            'slug': 'dummy-pants',
            'price': 33,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400',
            'image': None,
        },
    ]


def get_dummy_categories():
    """Возвращает заглушки категорий"""
    return [
        {
            'name': "Men's Clothing",
            'slug': 'mens-clothing',
            'image_url': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400',
            'image': None,
        },
        {
            'name': "Women's Clothing",
            'slug': 'womens-clothing',
            'image_url': 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=400',
            'image': None,
        },
        {
            'name': "Kids' Clothing",
            'slug': 'kids-clothing',
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400',
            'image': None,
        },
        {
            'name': 'Accessories',
            'slug': 'accessories',
            'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
            'image': None,
        },
    ]


def index(request):
    """Главная страница"""
    # Получаем товары из БД, если есть - иначе заглушки
    products = list(Product.objects.filter(is_active=True).order_by('-rating', '-reviews_count', '-created_at')[:8])
    if not products:
        products = get_dummy_products()
    
    # Получаем категории из БД, если есть - иначе заглушки
    categories = list(Category.objects.all().order_by('name')[:4])
    if not categories:
        categories = get_dummy_categories()
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'index.html', context)


def catalog(request):
    """Страница каталога"""
    # Получаем товары из БД, если есть - иначе заглушки
    products = list(Product.objects.filter(is_active=True).order_by('-created_at'))
    if not products:
        products = get_dummy_products()
    
    # Получаем категории из БД
    categories = list(Category.objects.all().order_by('name'))
    if not categories:
        categories = get_dummy_categories()
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'catalog.html', context)


def product_detail(request, slug=None):
    """Страница товара"""
    product = None
    related_products = []
    
    try:
        product = Product.objects.prefetch_related('images').get(slug=slug, is_active=True)
        
        # Получаем связанные товары из той же категории
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        
    except Product.DoesNotExist:
        # Если товар не найден, используем заглушку
        dummy_products = get_dummy_products()
        if dummy_products:
            # Создаем объект-заглушку с нужными атрибутами
            class DummyProduct:
                def __init__(self, data):
                    self.name = data.get('name', '')
                    self.slug = data.get('slug', '')
                    self.price = data.get('price', 0)
                    self.old_price = data.get('old_price')
                    self.description = 'Classic product description'
                    self.image_url = data.get('image_url')
                    self.image = None
                    self.available_sizes = 'S,M,L,XL'
                    self.available_colors = 'Черный, Белый, Синий, Красный'
                    self.stock = 10
                    self.rating = 4.0
                    self.reviews_count = 12
                    self.category = None
                    self.images = []
            
            product = DummyProduct(dummy_products[0])
    
    # Вычисляем скидку, если есть старая цена
    discount = None
    if product and hasattr(product, 'old_price') and product.old_price:
        discount = int(((product.old_price - product.price) / product.old_price) * 100)
    
    # Парсим доступные размеры
    sizes = []
    if product and hasattr(product, 'available_sizes'):
        sizes_str = str(product.available_sizes)
        # Если это одно значение (не содержит запятую), добавляем его как список
        if ',' in sizes_str:
            sizes = [s.strip() for s in sizes_str.split(',') if s.strip()]
        else:
            sizes = [sizes_str.strip()] if sizes_str.strip() else []
        # Если размеры все еще пусты, используем значения по умолчанию
        if not sizes:
            sizes = ['S', 'M', 'L', 'XL']
    
    # Парсим доступные цвета
    colors = []
    color_map = {
        'Черный': '#000000',
        'Белый': '#ffffff',
        'Синий': '#3498db',
        'Красный': '#e74c3c',
        'Зеленый': '#2ecc71',
        'Желтый': '#f1c40f',
        'Серый': '#95a5a6',
    }
    if product and hasattr(product, 'available_colors'):
        color_names = [c.strip() for c in str(product.available_colors).split(',') if c.strip()]
        colors = [{'name': name, 'code': color_map.get(name, '#000000')} for name in color_names]
    
    context = {
        'product': product,
        'related_products': related_products,
        'discount': discount,
        'sizes': sizes,
        'colors': colors,
    }
    return render(request, 'product.html', context)


def cart(request):
    """Страница корзины"""
    return render(request, 'cart.html')


def about(request):
    """Страница о нас"""
    return render(request, 'about.html')


def contact(request):
    """Страница контактов"""
    return render(request, 'contact.html')


def delivery(request):
    """Страница доставки"""
    return render(request, 'delivery.html')


