from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Product, Category


def get_dummy_products():
    """Возвращает заглушки товаров"""
    return [
        {
            'name': 'Деревянный обеденный стол',
            'slug': 'dummy-wooden-table',
            'price': 450,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop',
            'image': None,
        },
        {
            'name': 'Металлическая стеллажная система',
            'slug': 'dummy-metal-shelf',
            'price': 320,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1551292831-023188e34287?w=400&h=400&fit=crop',
            'image': None,
        },
        {
            'name': 'Деревянный шкаф',
            'slug': 'dummy-wooden-cabinet',
            'price': 680,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=400&fit=crop',
            'image': None,
        },
        {
            'name': 'Металлическая кровать',
            'slug': 'dummy-metal-bed',
            'price': 550,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=400&h=400&fit=crop',
            'image': None,
        },
        {
            'name': 'Деревянное кресло',
            'slug': 'dummy-wooden-chair',
            'price': 280,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1506439773649-6c5e9a6d8b12?w=400&h=400&fit=crop',
            'image': None,
        },
        {
            'name': 'Металлическая полка',
            'slug': 'dummy-metal-rack',
            'price': 190,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
            'image': None,
        },
        {
            'name': 'Деревянный комод',
            'slug': 'dummy-wooden-dresser',
            'price': 520,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&h=400&fit=crop',
            'image': None,
        },
        {
            'name': 'Металлическая конструкция',
            'slug': 'dummy-metal-structure',
            'price': 380,
            'old_price': None,
            'image_url': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=400&fit=crop',
            'image': None,
        },
    ]


def get_dummy_categories():
    """Возвращает заглушки категорий"""
    return [
        {
            'name': "Деревянная мебель",
            'slug': 'wooden-furniture',
            'image_url': 'https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?w=400&h=400&fit=crop',
            'image': None,
        },
        {
            'name': "Металлические изделия",
            'slug': 'metal-products',
            'image_url': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400&h=400&fit=crop',
            'image': None,
        },
        {
            'name': "Столы и стулья",
            'slug': 'tables-chairs',
            'image_url': 'https://images.unsplash.com/photo-1538688525198-9b88f6f53126?w=400&h=400&fit=crop',
            'image': None,
        },
        {
            'name': 'Шкафы и комоды',
            'slug': 'cabinets-dressers',
            'image_url': 'https://images.unsplash.com/photo-1556912172-45b7abe8b7e1?w=400&h=400&fit=crop',
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
    # Получаем товары из БД
    products_queryset = Product.objects.filter(is_active=True)
    
    # Фильтрация по категории
    category_slug = request.GET.get('category', None)
    if category_slug:
        products_queryset = products_queryset.filter(category__slug=category_slug)
    
    # Фильтрация по цене
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    if min_price:
        try:
            products_queryset = products_queryset.filter(price__gte=float(min_price))
        except (ValueError, TypeError):
            pass
    if max_price:
        try:
            products_queryset = products_queryset.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass
    
    # Поиск
    search_query = request.GET.get('search', None)
    if search_query:
        products_queryset = products_queryset.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = {
        'popularity': '-rating',
        'price_low': 'price',
        'price_high': '-price',
        'newest': '-created_at',
    }
    sort_order = valid_sorts.get(sort_by, '-created_at')
    products_queryset = products_queryset.order_by(sort_order)
    
    # Если нет товаров в БД, используем заглушки
    use_dummy = False
    if not products_queryset.exists():
        products_queryset = None
        use_dummy = True
    
    # Пагинация
    if use_dummy:
        # Для заглушек создаем простой список
        dummy_products = get_dummy_products()
        paginator = Paginator(dummy_products, 12)  # 12 товаров на страницу
    else:
        paginator = Paginator(products_queryset, 12)  # 12 товаров на страницу
    
    page = request.GET.get('page', 1)
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    # Получаем категории из БД
    categories = list(Category.objects.all().order_by('name'))
    if not categories:
        categories = get_dummy_categories()
    
    context = {
        'products': products_page,
        'categories': categories,
        'current_category': category_slug,
        'current_sort': sort_by,
        'current_search': search_query,
        'min_price': min_price,
        'max_price': max_price,
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
                    self.description = 'Качественное изделие из дерева или металла. Прочная конструкция и долговечность.'
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


