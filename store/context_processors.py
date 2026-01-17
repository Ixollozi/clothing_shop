"""
Context processors для передачи конфигурации в шаблоны
"""
from .config_loader import get_config
from .models import Partner, Feature


def store_config(request):
    """
    Передает конфигурацию магазина во все шаблоны
    """
    config = get_config()
    # Получаем партнеров из БД вместо конфига
    partners = Partner.objects.filter(is_active=True).order_by('order', 'name')
    # Получаем features из БД вместо конфига
    features = Feature.objects.filter(is_active=True).order_by('order', 'title')
    
    return {
        'store_config': config,
        'store_name': config.get('store', {}).get('name', 'Fashion Store'),
        'store_title': config.get('store', {}).get('title', 'Fashion Store'),
        'store_description': config.get('store', {}).get('description', ''),
        'contact_info': config.get('contact', {}),
        'social_links': config.get('social', {}),
        'partners': partners,  # Теперь из БД
        'features': features,  # Теперь из БД
        'about_info': config.get('about', {}),
        'hero_config': config.get('hero', {}),
        'seo_config': config.get('seo', {}),
        'theme_config': config.get('theme', {}),
    }

