from django.shortcuts import render


def index(request):
    """Главная страница"""
    return render(request, 'index.html')


def catalog(request):
    """Страница каталога"""
    return render(request, 'catalog.html')


def product_detail(request, slug=None):
    """Страница товара"""
    return render(request, 'product.html')


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

