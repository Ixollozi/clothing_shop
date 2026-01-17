from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Product, Category, Cart, CartItem


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
    
    # Фильтрация по размеру
    size_filter = request.GET.get('size', None)
    if size_filter:
        # Ищем товары, у которых в available_sizes есть указанный размер
        products_queryset = products_queryset.filter(
            Q(available_sizes__icontains=size_filter)
        )
    
    # Фильтрация по цвету
    color_filter = request.GET.get('color', None)
    if color_filter:
        # Маппинг цветов из hex в названия
        color_map = {
            '#000': 'Черный',
            '#000000': 'Черный',
            '#fff': 'Белый',
            '#ffffff': 'Белый',
            '#e74c3c': 'Красный',
            '#3498db': 'Синий',
            '#2ecc71': 'Зеленый',
            '#f39c12': 'Желтый',
        }
        color_name = color_map.get(color_filter.lower(), color_filter)
        # Ищем товары, у которых в available_colors есть указанный цвет
        products_queryset = products_queryset.filter(
            Q(available_colors__icontains=color_name)
        )
    
    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    
    # Если нет товаров в БД, используем заглушки
    use_dummy = False
    if not products_queryset.exists():
        products_queryset = None
        use_dummy = True
    
    # Применяем сортировку
    if use_dummy:
        # Для заглушек создаем простой список и сортируем его
        dummy_products = get_dummy_products()
        
        # Добавляем поля для сортировки и фильтрации к заглушкам
        for i, product in enumerate(dummy_products):
            product['rating'] = 4.0 + (i % 3) * 0.5  # Разные рейтинги для сортировки
            product['reviews_count'] = 10 + i * 2  # Разное количество отзывов
            product['created_at'] = i  # Индекс как дата создания (меньше = новее)
            product['available_sizes'] = ['XS', 'S', 'M', 'L', 'XL'][i % 5]  # Разные размеры
            product['available_colors'] = ['Черный', 'Белый', 'Синий', 'Красный', 'Зеленый', 'Желтый'][i % 6]  # Разные цвета
        
        # Применяем фильтры к заглушкам
        if size_filter:
            dummy_products = [p for p in dummy_products if size_filter in str(p.get('available_sizes', ''))]
        
        if color_filter:
            # Маппинг цветов из hex в названия
            color_map = {
                '#000': 'Черный',
                '#000000': 'Черный',
                '#fff': 'Белый',
                '#ffffff': 'Белый',
                '#e74c3c': 'Красный',
                '#3498db': 'Синий',
                '#2ecc71': 'Зеленый',
                '#f39c12': 'Желтый',
            }
            color_name = color_map.get(color_filter.lower(), color_filter)
            dummy_products = [p for p in dummy_products if color_name in str(p.get('available_colors', ''))]
        
        # Сортируем заглушки
        if sort_by == 'popularity':
            # По популярности: сначала по рейтингу, потом по количеству отзывов
            dummy_products.sort(key=lambda x: (-x['rating'], -x['reviews_count']))
        elif sort_by == 'price_low':
            # По цене: от низкой к высокой
            dummy_products.sort(key=lambda x: x['price'])
        elif sort_by == 'price_high':
            # По цене: от высокой к низкой
            dummy_products.sort(key=lambda x: -x['price'])
        elif sort_by == 'newest':
            # По новизне: сначала новые (меньший индекс = новее)
            dummy_products.sort(key=lambda x: x['created_at'])
        else:
            # По умолчанию: по новизне
            dummy_products.sort(key=lambda x: x['created_at'])
        
        paginator = Paginator(dummy_products, 12)  # 12 товаров на страницу
    else:
        # Сортировка для реальных товаров из БД
        if sort_by == 'popularity':
            # По популярности: сначала по рейтингу, потом по количеству отзывов, потом по дате создания
            products_queryset = products_queryset.order_by('-rating', '-reviews_count', '-created_at')
        elif sort_by == 'price_low':
            # По цене: от низкой к высокой
            products_queryset = products_queryset.order_by('price', '-created_at')
        elif sort_by == 'price_high':
            # По цене: от высокой к низкой
            products_queryset = products_queryset.order_by('-price', '-created_at')
        elif sort_by == 'newest':
            # По новизне: сначала новые
            products_queryset = products_queryset.order_by('-created_at')
        else:
            # По умолчанию: по новизне
            products_queryset = products_queryset.order_by('-created_at')
        
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
        'current_size': size_filter,
        'current_color': color_filter,
    }
    return render(request, 'catalog.html', context)


def product_detail(request, slug=None):
    """Страница товара"""
    product = None
    related_products = []
    
    # Сначала пытаемся найти товар в БД
    if slug:
        try:
            product = Product.objects.prefetch_related('images').get(slug=slug, is_active=True)
            
            # Получаем связанные товары из той же категории
            if product.category:
                related_products = Product.objects.filter(
                    category=product.category,
                    is_active=True
                ).exclude(id=product.id)[:4]
            else:
                # Если нет категории, берем любые активные товары
                related_products = Product.objects.filter(is_active=True).exclude(id=product.id)[:4]
        except Product.DoesNotExist:
            pass
    
    # Если товар не найден в БД, ищем в заглушках по slug
    if not product:
        dummy_products = get_dummy_products()
        if slug:
            # Ищем заглушку по slug
            dummy_product_data = next((p for p in dummy_products if p.get('slug') == slug), None)
        else:
            # Берем первую заглушку
            dummy_product_data = dummy_products[0] if dummy_products else None
        
        if dummy_product_data:
            # Создаем объект-заглушку с нужными атрибутами
            class DummyProduct:
                def __init__(self, data):
                    self.id = None  # Нет ID для заглушек
                    self.name = data.get('name', '')
                    self.slug = data.get('slug', '')
                    self.price = data.get('price', 0)
                    self.old_price = data.get('old_price')
                    self.description = 'Classic product description. This is a high-quality product with excellent materials and craftsmanship.'
                    self.image_url = data.get('image_url')
                    self.image = None
                    self.available_sizes = 'S,M,L,XL'
                    self.available_colors = 'Черный, Белый, Синий, Красный'
                    self.stock = 10
                    self.rating = 4.0
                    self.reviews_count = 12
                    self.category = None
                    self.images = []
            
            product = DummyProduct(dummy_product_data)
            
            # Для связанных товаров берем другие заглушки
            related_products_data = [p for p in dummy_products if p.get('slug') != product.slug][:4]
            related_products = []
            for data in related_products_data:
                related_products.append(DummyProduct(data))
    
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
    
    # Получаем features товара из базы данных
    from .models import ProductFeatureConfig
    product_features = ProductFeatureConfig.objects.filter(is_active=True).order_by('order', 'title')
    
    context = {
        'product': product,
        'related_products': related_products,
        'discount': discount,
        'sizes': sizes,
        'colors': colors,
        'product_features': product_features,
    }
    return render(request, 'product.html', context)


def cart(request):
    """Страница корзины"""
    # Получаем или создаем корзину для текущей сессии
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)


def about(request):
    """Страница о нас"""
    from .models import AboutStat, AboutConfig
    stats = AboutStat.objects.filter(is_active=True).order_by('order', 'created_at')
    about_config = AboutConfig.objects.filter(is_active=True).first()
    context = {
        'stats': stats,
        'about_config': about_config,
    }
    return render(request, 'about.html', context)


def contact(request):
    """Страница контактов"""
    return render(request, 'contact.html')


def delivery(request):
    """Страница доставки"""
    return render(request, 'delivery.html')


