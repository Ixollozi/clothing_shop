"""
Настройки переводов для моделей
"""
from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, Partner


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'available_colors')


@register(Partner)
class PartnerTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


