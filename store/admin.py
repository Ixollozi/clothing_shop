from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from modeltranslation.admin import TabbedTranslationAdmin
from modeltranslation.translator import translator
from .models import Category, Product, ProductImage, Cart, CartItem, Order, OrderItem, Partner

# Импортируем переводы перед регистрацией админки
try:
    from . import translation
except ImportError:
    pass


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'slug', 'image_preview', 'products_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Изображение', {
            'fields': ('image', 'image_url', 'image_preview')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image_url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'

    def products_count(self, obj):
        count = obj.products.count()
        url = reverse('admin:store_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{} товаров</a>', url, count)
    products_count.short_description = 'Товаров'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_preview', 'created_at')
    readonly_fields = ('image_preview', 'created_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 80px; max-height: 80px;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'category', 'price_display', 'old_price_display', 'stock', 'is_active', 'image_preview', 'created_at']
    list_filter = ['category', 'is_active', 'created_at', 'rating']
    search_fields = ['name', 'description', 'available_colors']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'image_preview', 'image_url_preview', 'discount_percent', 'colors_help']
    inlines = [ProductImageInline]
    list_editable = ['is_active', 'stock']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Цены', {
            'fields': ('price', 'old_price', 'discount_percent')
        }),
        ('Изображения', {
            'fields': ('image', 'image_preview', 'image_url', 'image_url_preview')
        }),
        ('Характеристики', {
            'fields': ('available_sizes', 'available_colors', 'colors_help', 'stock', 'is_active'),
            'description': 'Укажите доступные размеры и цвета для товара'
        }),
        ('Рейтинг', {
            'fields': ('rating', 'reviews_count')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def colors_help(self, obj):
        """Подсказка о доступных цветах"""
        colors_list = [
            ('Черный', '#000000'),
            ('Белый', '#FFFFFF'),
            ('Синий', '#2196F3'),
            ('Красный', '#F44336'),
            ('Зеленый', '#4CAF50'),
            ('Желтый', '#FFEB3B'),
            ('Серый', '#9E9E9E'),
        ]
        html = '<div style="margin-top: 10px; padding: 10px; background: #f5f5f5; border-radius: 4px;">'
        html += '<strong>Доступные цвета:</strong><br>'
        html += '<div style="margin-top: 8px; display: flex; flex-wrap: wrap; gap: 10px;">'
        for color_name, color_code in colors_list:
            html += f'''
            <div style="display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px; background: white; border-radius: 4px; border: 1px solid #ddd;">
                <span style="display: inline-block; width: 20px; height: 20px; border-radius: 50%; background-color: {color_code}; border: 1px solid #ccc;"></span>
                <span>{color_name}</span>
            </div>
            '''
        html += '</div>'
        html += '<p style="margin-top: 10px; margin-bottom: 0; color: #666; font-size: 0.9em;">'
        html += '💡 <strong>Подсказка:</strong> Указывайте цвета через запятую, например: "Черный, Белый, Синий"'
        html += '</p></div>'
        return mark_safe(html)
    colors_help.short_description = 'Подсказка по цветам'

    def price_display(self, obj):
        return f"${obj.price}"
    price_display.short_description = 'Цена'

    def old_price_display(self, obj):
        if obj.old_price:
            return format_html('<span style="text-decoration: line-through; color: #999;">${}</span>', obj.old_price)
        return "-"
    old_price_display.short_description = 'Старая цена'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 150px; max-height: 150px;" />', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-width: 150px; max-height: 150px;" />', obj.image_url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'

    def image_url_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-width: 150px; max-height: 150px;" />', obj.image_url)
        return "Нет URL изображения"
    image_url_preview.short_description = 'Превью URL'

    def discount_percent(self, obj):
        if obj.old_price and obj.old_price > obj.price:
            discount = ((obj.old_price - obj.price) / obj.old_price) * 100
            return format_html('<span style="color: #d32f2f; font-weight: bold;">-{}%</span>', round(discount, 0))
        return "-"
    discount_percent.short_description = 'Скидка'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'created_at']
    list_filter = ['created_at', 'product__category']
    search_fields = ['product__name']
    readonly_fields = ['image_preview', 'created_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'items_count_display', 'total_display', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['session_key']
    readonly_fields = ['created_at', 'updated_at', 'items_count_display', 'total_display']
    fieldsets = (
        ('Информация', {
            'fields': ('session_key', 'items_count_display', 'total_display')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def items_count_display(self, obj):
        count = obj.items_count
        url = reverse('admin:store_cartitem_changelist') + f'?cart__id__exact={obj.id}'
        return format_html('<a href="{}">{} товаров</a>', url, count)
    items_count_display.short_description = 'Товаров в корзине'

    def total_display(self, obj):
        return f"${obj.total}"
    total_display.short_description = 'Итого'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'size', 'color', 'total_display', 'created_at']
    list_filter = ['cart', 'created_at', 'product__category']
    search_fields = ['product__name', 'cart__session_key']
    readonly_fields = ['total_display', 'created_at', 'updated_at']

    def total_display(self, obj):
        return f"${obj.total}"
    total_display.short_description = 'Итого'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_display']
    fields = ('product', 'quantity', 'price', 'size', 'color', 'total_display')
    can_delete = False

    def total_display(self, obj):
        if obj and obj.pk:
            return f"${obj.total:.2f}"
        return "-"
    total_display.short_description = 'Итого'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'phone', 'total_display', 'status', 'status_badge', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'city', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    readonly_fields = ['created_at', 'updated_at', 'total_display', 'items_count_display', 'status_badge']
    inlines = [OrderItemInline]
    list_editable = ['status']
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('status', 'payment_method', 'total_display', 'items_count_display')
        }),
        ('Информация о клиенте', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Адрес доставки', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Дополнительно', {
            'fields': ('session_key', 'notes')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = 'Клиент'

    def total_display(self, obj):
        return format_html('<strong style="font-size: 16px; color: #1976d2;">${}</strong>', obj.total)
    total_display.short_description = 'Итого'

    def status_badge(self, obj):
        colors = {
            'pending': '#ff9800',
            'processing': '#2196f3',
            'shipped': '#9c27b0',
            'delivered': '#4caf50',
            'cancelled': '#f44336',
        }
        color = colors.get(obj.status, '#757575')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'

    def items_count_display(self, obj):
        return f"{obj.items.count()} товаров"
    items_count_display.short_description = 'Товаров в заказе'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'size', 'color', 'total_display']
    list_filter = ['order__status', 'order__created_at', 'product__category']
    search_fields = ['product__name', 'order__first_name', 'order__last_name', 'order__email']
    readonly_fields = ['total_display']

    def total_display(self, obj):
        if obj and obj.pk:
            return f"${obj.total:.2f}"
        return "-"
    total_display.short_description = 'Итого'


# Настройка админ-сайта
admin.site.site_header = "Fashion Store - Администрирование"
admin.site.site_title = "Fashion Store Admin"
admin.site.index_title = "Панель управления"
admin.site.index_template = 'admin/index.html'


@admin.register(Partner)
class PartnerAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'icon', 'logo_preview', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at', 'updated_at', 'logo_preview']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'icon', 'url', 'description', 'is_active', 'order')
        }),
        ('Логотип', {
            'fields': ('logo', 'logo_preview')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.logo.url)
        return "Нет логотипа"
    logo_preview.short_description = 'Превью логотипа'
