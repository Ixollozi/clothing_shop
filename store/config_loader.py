"""
Утилита для загрузки конфигурации из config.json
"""
import json
import os
from pathlib import Path

# Используем BASE_DIR напрямую, чтобы избежать циклических импортов
BASE_DIR = Path(__file__).resolve().parent.parent


def load_config():
    """
    Загружает конфигурацию из config.json
    """
    config_path = BASE_DIR / 'config.json'
    
    if not config_path.exists():
        # Возвращаем конфигурацию по умолчанию
        return get_default_config()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading config.json: {e}")
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

