"""
Кастомные теги для работы с переводами
"""
from django import template
from django.utils.translation import get_language, activate, gettext_lazy as _

register = template.Library()


@register.simple_tag(takes_context=True)
def get_current_language(context):
    """Возвращает текущий язык"""
    return get_language()


@register.simple_tag
def get_available_languages():
    """Возвращает список доступных языков"""
    from django.conf import settings
    return settings.LANGUAGES


