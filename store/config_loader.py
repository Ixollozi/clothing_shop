"""
Утилита для загрузки конфигурации из моделей или config.json
"""
import json
import os
from pathlib import Path

# Используем BASE_DIR напрямую, чтобы избежать циклических импортов
BASE_DIR = Path(__file__).resolve().parent.parent


def load_config_from_models():
    """
    Загружает конфигурацию из отдельных моделей (StoreConfig, ContactConfig и т.д.)
    Самый высокий приоритет
    """
    try:
        from .models import (
            StoreConfig, ContactConfig, SocialConfig, HeroConfig,
            Feature, AboutConfig, SEOConfig, ThemeConfig
        )
        
        config = {}
        
        # Store
        store = StoreConfig.objects.filter(is_active=True).first()
        if store:
            config['store'] = {
                'name': store.name,
                'title': store.title,
                'description': store.description,
                'logo': store.logo.url if store.logo else '',
                'favicon': store.favicon.url if store.favicon else '',
            }
        
        # Contact
        contact = ContactConfig.objects.filter(is_active=True).first()
        if contact:
            config['contact'] = {
                'phone': contact.phone,
                'email': contact.email,
                'address': {
                    'city': contact.address_city,
                    'street': contact.address_street,
                    'full': contact.address_full,
                },
                'working_hours': {
                    'weekdays': contact.working_hours_weekdays,
                    'weekend': contact.working_hours_weekend,
                }
            }
        
        # Social
        social = SocialConfig.objects.filter(is_active=True).first()
        if social:
            config['social'] = {
                'instagram': social.instagram,
                'facebook': social.facebook,
                'twitter': social.twitter,
                'vk': social.vk,
                'telegram': social.telegram,
                'whatsapp': social.whatsapp,
            }
        
        # Hero
        hero = HeroConfig.objects.filter(is_active=True).first()
        if hero:
            config['hero'] = {
                'title': hero.title,
                'subtitle': hero.subtitle,
                'button_text': hero.button_text,
                'background_image': hero.background_image.url if hero.background_image else '',
            }
        
        # Features
        features = Feature.objects.filter(is_active=True).order_by('order', 'title')
        if features.exists():
            config['features'] = [
                {
                    'icon': f.icon,
                    'title': f.title,
                    'description': f.description,
                }
                for f in features
            ]
        
        # About
        about = AboutConfig.objects.filter(is_active=True).first()
        if about:
            config['about'] = {
                'title': about.title,
                'description': about.description,
                'mission': about.mission,
                'vision': about.vision,
                'values': about.get_values_list(),
            }
        
        # SEO
        seo = SEOConfig.objects.filter(is_active=True).first()
        if seo:
            config['seo'] = {
                'meta_title': seo.meta_title,
                'meta_description': seo.meta_description,
                'meta_keywords': seo.meta_keywords,
            }
        
        # Theme
        theme = ThemeConfig.objects.filter(is_active=True).first()
        if theme:
            config['theme'] = {
                'primary_color': theme.primary_color,
                'secondary_color': theme.secondary_color,
                'text_color': theme.text_color,
                'background_color': theme.background_color,
            }
        
        # Если есть хотя бы одна секция, возвращаем конфигурацию
        if config:
            return config
            
    except Exception as e:
        # Если таблицы еще не созданы или другая ошибка, игнорируем
        pass
    return None


def load_config_from_db():
    """
    Загружает конфигурацию из базы данных (модель Config - JSON)
    Второй приоритет
    """
    try:
        # Импортируем здесь, чтобы избежать циклических импортов
        from .models import Config
        config = Config.get_active_config()
        if config:
            return config
    except Exception as e:
        # Если таблица еще не создана или другая ошибка, игнорируем
        pass
    return None


def load_config_from_file():
    """
    Загружает конфигурацию из config.json
    """
    config_path = BASE_DIR / 'config.json'
    
    if not config_path.exists():
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading config.json: {e}")
        return None


def load_config():
    """
    Загружает конфигурацию с приоритетом:
    1. Из отдельных моделей (StoreConfig, ContactConfig и т.д.) - самый высокий приоритет
    2. Из базы данных (модель Config - JSON)
    3. Из config.json
    4. Конфигурация по умолчанию
    """
    # Сначала пытаемся загрузить из отдельных моделей
    config = load_config_from_models()
    if config:
        # Дополняем конфигурацию из config.json для секций, которых нет в моделях (например, django)
        file_config = load_config_from_file()
        if file_config:
            # Добавляем секции, которых нет в моделях
            for key, value in file_config.items():
                if key not in config:
                    config[key] = value
        return config
    
    # Затем из модели Config (JSON)
    config = load_config_from_db()
    if config:
        return config
    
    # Затем из файла
    config = load_config_from_file()
    if config:
        return config
    
    # Иначе используем конфигурацию по умолчанию
    return get_default_config()


def get_default_config():
    """
    Возвращает конфигурацию по умолчанию
    """
    return {
        "store": {
            "name": "Fashion Store",
            "title": "Fashion Store - Online Clothing Store",
            "description": "Your reliable partner in the world of fashion. Quality clothing at affordable prices.",
        },
        "contact": {
            "phone": "+7 (800) 123-45-67",
            "email": "info@fashionstore.ru",
            "address": {
                "city": "Tashkent",
                "street": "Example Street, 1",
                "full": "Tashkent, Example Street, 1"
            },
        },
        "social": {
            "instagram": "#",
            "facebook": "#",
            "twitter": "#",
            "vk": "#",
        },
        "partners": [],
        "features": [],
        "about": {
            "title": "About Us",
            "description": "We are a modern fashion store.",
        },
        "django": {
            "debug": True,
            "allowed_hosts": ["*"],
            "secret_key": "django-insecure-your-secret-key-change-in-production",
            "time_zone": "Asia/Tashkent",
            "language_code": "ru",
            "languages": ["ru", "en", "uz"],
            "default_language": "ru",
        },
    }


# Кэшируем конфигурацию
_config_cache = None


def get_config():
    """
    Получает конфигурацию (с кэшированием)
    """
    global _config_cache
    if _config_cache is None:
        _config_cache = load_config()
    return _config_cache


def reload_config():
    """
    Перезагружает конфигурацию (полезно при изменении config.json)
    """
    global _config_cache
    _config_cache = None
    return get_config()


def get_django_config():
    """
    Получает настройки Django из config.json
    """
    config = get_config()
    return config.get('django', {})

