from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from django import forms
from django.forms.widgets import TextInput
from modeltranslation.admin import TabbedTranslationAdmin
from modeltranslation.translator import translator
from .models import (
    Category, Product, ProductImage, Cart, CartItem, Order, OrderItem, Partner, Config,
    StoreConfig, ContactConfig, SocialConfig, HeroConfig, Feature, AboutConfig, SEOConfig, ThemeConfig,
    ProductFeatureConfig, AboutStat, TelegramConfig, ContactMessage, FAQ
)

class ColorPaletteWidget(TextInput):
    """
    Виджет выбора цвета для админки:
    - нативный color picker
    - HEX поле
    - кликабельная палитра
    - превью выбранного цвета
    """

    PRESET_COLORS = [
        # Neutrals
        "#000000", "#1f2937", "#374151", "#6b7280", "#9ca3af", "#d1d5db", "#e5e7eb", "#ffffff",
        # Brand-friendly
        "#1976d2", "#0ea5e9", "#22c55e", "#f59e0b", "#ef4444", "#a855f7", "#ec4899", "#14b8a6",
        # Warm palette
        "#7a4a2a", "#c49a63", "#f3e6d6", "#2d2d2d",
    ]

    def __init__(self, attrs=None):
        base = {"class": "vTextField admin-color-hex", "placeholder": "#1976d2"}
        if attrs:
            base.update(attrs)
        super().__init__(attrs=base)

    def format_value(self, value):
        if not value:
            return ""
        return str(value)

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        palette = "".join(
            f'<button type="button" class="admin-color-swatch" data-color="{c}" style="background:{c}" aria-label="{c}"></button>'
            for c in self.PRESET_COLORS
        )
        color_value = self.format_value(value) or "#000000"
        return mark_safe(
            f"""
            <div class="admin-color-field" data-color-field>
              <div class="admin-color-row">
                <input type="color" class="admin-color-picker" value="{color_value}" aria-label="Color picker" />
                {html}
                <span class="admin-color-preview" title="{color_value}">
                  <span class="admin-color-preview-swatch" style="background:{color_value}"></span>
                  <span class="admin-color-preview-hex">{color_value}</span>
                </span>
              </div>
              <div class="admin-color-palette" role="list" aria-label="Палитра">
                {palette}
              </div>
            </div>
            """
        )


class ThemeConfigAdminForm(forms.ModelForm):
    class Meta:
        model = ThemeConfig
        fields = "__all__"
        widgets = {
            "primary_color": ColorPaletteWidget(),
            "secondary_color": ColorPaletteWidget(),
            "text_color": ColorPaletteWidget(),
            "background_color": ColorPaletteWidget(),
        }


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
    exclude = ('available_sizes',)
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
            'fields': ('available_colors', 'colors_help', 'stock', 'is_active'),
            'description': 'Укажите доступные цвета для товара'
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
        return f"{obj.price:,.0f} сум".replace(',', ' ')
    price_display.short_description = 'Цена'

    def old_price_display(self, obj):
        if obj.old_price:
            return format_html('<span style="text-decoration: line-through; color: #999;">{} сум</span>', f"{obj.old_price:,.0f}".replace(',', ' '))
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
        return f"{obj.total:,.0f} сум".replace(',', ' ')
    total_display.short_description = 'Итого'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    exclude = ('size',)
    list_display = ['product', 'cart', 'quantity', 'color', 'total_display', 'created_at']
    list_filter = ['cart', 'created_at', 'product__category']
    search_fields = ['product__name', 'cart__session_key']
    readonly_fields = ['total_display', 'created_at', 'updated_at']

    def total_display(self, obj):
        return f"{obj.total:,.0f} сум".replace(',', ' ')
    total_display.short_description = 'Итого'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_display']
    fields = ('product', 'quantity', 'price', 'color', 'total_display')
    can_delete = False

    def total_display(self, obj):
        if obj and obj.pk:
            return f"{obj.total:,.0f} сум".replace(',', ' ')
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
        total_formatted = f"{obj.total:,.0f}".replace(',', ' ')
        return format_html('<strong style="font-size: 16px; color: #1976d2;">{} сум</strong>', total_formatted)
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
    exclude = ('size',)
    list_display = ['order', 'product', 'quantity', 'price', 'color', 'total_display']
    list_filter = ['order__status', 'order__created_at', 'product__category']
    search_fields = ['product__name', 'order__first_name', 'order__last_name', 'order__email']
    readonly_fields = ['total_display']

    def total_display(self, obj):
        if obj and obj.pk:
            return f"{obj.total:,.0f} сум".replace(',', ' ')
        return "-"
    total_display.short_description = 'Итого'


# Настройка админ-сайта
admin.site.site_header = "Администрирование"
admin.site.site_title = "Admin"
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


class ConfigAdminForm(forms.ModelForm):
    """
    Форма для редактирования конфигурации с валидацией JSON
    """
    class Meta:
        model = Config
        fields = '__all__'
        widgets = {
            'config_data': forms.Textarea(attrs={
                'rows': 30,
                'style': 'font-family: monospace; font-size: 12px;',
                'placeholder': 'Введите валидный JSON...'
            }),
        }

    def clean_config_data(self):
        config_data = self.cleaned_data.get('config_data')
        if isinstance(config_data, str):
            import json
            try:
                config_data = json.loads(config_data)
            except json.JSONDecodeError as e:
                raise forms.ValidationError(f'Невалидный JSON: {e}')
        return config_data


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    form = ConfigAdminForm
    list_display = ['key', 'is_active', 'config_preview', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['key', 'description']
    readonly_fields = ['created_at', 'updated_at', 'config_info']
    fieldsets = (
        ('Основная информация', {
            'fields': ('key', 'is_active', 'description')
        }),
        ('Конфигурация', {
            'fields': ('config_data', 'config_info'),
            'description': 'Введите конфигурацию в формате JSON. При сохранении она будет синхронизирована с config.json'
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def config_preview(self, obj):
        """Показывает краткую информацию о конфигурации"""
        if obj.config_data:
            sections = list(obj.config_data.keys())[:5]
            sections_str = ', '.join(sections)
            if len(obj.config_data) > 5:
                sections_str += f' ... (+{len(obj.config_data) - 5} секций)'
            return format_html('<span style="font-family: monospace;">{}</span>', sections_str)
        return "Пустая конфигурация"
    config_preview.short_description = 'Секции конфигурации'

    def config_info(self, obj):
        """Показывает информацию о структуре конфигурации"""
        if not obj.config_data:
            return "Конфигурация пуста"
        
        import json
        try:
            config_str = json.dumps(obj.config_data, ensure_ascii=False, indent=2)
            size = len(config_str)
            sections = list(obj.config_data.keys())
            
            info = f"""
            <div style="background: #f5f5f5; padding: 10px; border-radius: 5px; margin: 10px 0;">
                <strong>Информация о конфигурации:</strong><br>
                • Секций: {len(sections)}<br>
                • Размер: {size} символов<br>
                • Секции: {', '.join(sections[:10])}{'...' if len(sections) > 10 else ''}
            </div>
            """
            return mark_safe(info)
        except Exception as e:
            return format_html('<span style="color: red;">Ошибка: {}</span>', str(e))
    config_info.short_description = 'Информация'

    def save_model(self, request, obj, form, change):
        """Переопределяем сохранение для синхронизации с файлом"""
        super().save_model(request, obj, form, change)
        if obj.is_active:
            obj.sync_to_file()
            self.message_user(request, 'Конфигурация сохранена и синхронизирована с config.json')


@admin.register(StoreConfig)
class StoreConfigAdmin(TabbedTranslationAdmin):
    def has_module_permission(self, request):
        """Скрываем из списка админки, но оставляем доступ к редактированию"""
        return False
    list_display = ['name', 'is_active', 'updated_at']
    readonly_fields = ['updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'title', 'description', 'is_active')
        }),
        ('Изображения', {
            'fields': ('logo', 'favicon')
        }),
        ('Даты', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContactConfig)
class ContactConfigAdmin(TabbedTranslationAdmin):
    def has_module_permission(self, request):
        """Скрываем из списка админки, но оставляем доступ к редактированию"""
        return False
    list_display = ['phone', 'email', 'is_active', 'updated_at']
    readonly_fields = ['updated_at']
    fieldsets = (
        ('Контактная информация', {
            'fields': ('phone', 'email', 'is_active')
        }),
        ('Адрес', {
            'fields': ('address_city', 'address_street', 'address_full', 'map_url')
        }),
        ('Рабочие часы', {
            'fields': ('working_hours_weekdays', 'working_hours_weekend')
        }),
        ('Даты', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SocialConfig)
class SocialConfigAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        """Скрываем из списка админки, но оставляем доступ к редактированию"""
        return False
    list_display = ['instagram', 'facebook', 'telegram', 'is_active', 'updated_at']
    readonly_fields = ['updated_at']
    fieldsets = (
        ('Социальные сети', {
            'fields': ('instagram', 'facebook', 'twitter', 'vk', 'telegram', 'whatsapp', 'is_active')
        }),
        ('Даты', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(HeroConfig)
class HeroConfigAdmin(TabbedTranslationAdmin):
    def has_module_permission(self, request):
        """Скрываем из списка админки, но оставляем доступ к редактированию"""
        return False
    list_display = ['title', 'subtitle', 'is_active', 'updated_at']
    readonly_fields = ['updated_at', 'background_image_preview']
    fieldsets = (
        ('Содержимое', {
            'fields': ('title', 'subtitle', 'button_text', 'is_active')
        }),
        ('Изображение', {
            'fields': ('background_image', 'background_image_url', 'background_image_preview'),
            'description': 'Загрузите изображение или укажите URL. Приоритет у загруженного изображения.'
        }),
        ('Даты', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def background_image_preview(self, obj):
        """Показывает превью фонового изображения"""
        if obj.pk:
            if obj.background_image:
                return format_html('<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 5px; margin-top: 10px;" />', obj.background_image.url)
            elif obj.background_image_url:
                return format_html('<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 5px; margin-top: 10px;" />', obj.background_image_url)
        return "Сохраните для предпросмотра"
    background_image_preview.short_description = 'Превью изображения'


@admin.register(Feature)
class FeatureAdmin(TabbedTranslationAdmin):
    def has_module_permission(self, request):
        """Скрываем из списка админки, но оставляем доступ к редактированию"""
        return False
    list_display = ['title', 'icon', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'icon', 'order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AboutConfig)
class AboutConfigAdmin(TabbedTranslationAdmin):
    def has_module_permission(self, request):
        """Скрываем из списка админки, но оставляем доступ к редактированию"""
        return False
    list_display = ['title', 'is_active', 'updated_at']
    readonly_fields = ['updated_at', 'image_preview']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Миссия и видение', {
            'fields': ('mission', 'vision')
        }),
        ('Ценности', {
            'fields': ('values',),
            'description': 'Указывайте каждое значение с новой строки'
        }),
        ('Изображение', {
            'fields': ('image', 'image_url', 'image_preview'),
            'description': 'Загрузите изображение или укажите URL. Приоритет у загруженного изображения.'
        }),
        ('Даты', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Показывает превью изображения"""
        if obj.pk:
            if obj.image:
                return format_html('<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 5px; margin-top: 10px;" />', obj.image.url)
            elif obj.image_url:
                return format_html('<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 5px; margin-top: 10px;" />', obj.image_url)
        return "Сохраните для предпросмотра"
    image_preview.short_description = 'Превью изображения'


@admin.register(AboutStat)
class AboutStatAdmin(TabbedTranslationAdmin):
    def has_module_permission(self, request):
        """Скрываем из списка админки"""
        return False
    
    list_display = ['value', 'label', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['value', 'label']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('value', 'label', 'order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SEOConfig)
class SEOConfigAdmin(TabbedTranslationAdmin):
    def has_module_permission(self, request):
        """Скрываем из списка админки, но оставляем доступ к редактированию"""
        return False
    list_display = ['meta_title', 'is_active', 'updated_at']
    readonly_fields = ['updated_at']
    fieldsets = (
        ('SEO настройки', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'is_active')
        }),
        ('Даты', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ThemeConfig)
class ThemeConfigAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        """Скрываем из списка админки, но оставляем доступ к редактированию"""
        return False
    list_display = ['primary_color', 'secondary_color', 'is_active', 'updated_at']
    readonly_fields = ['updated_at', 'color_preview']
    form = ThemeConfigAdminForm
    fieldsets = (
        ('Цвета темы', {
            'fields': ('primary_color', 'secondary_color', 'text_color', 'background_color', 'is_active', 'color_preview')
        }),
        ('Даты', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    class Media:
        css = {
            "all": ("admin/css/custom_admin.css",)
        }
        js = ("admin/js/theme_palette.js",)

    def color_preview(self, obj):
        """Показывает превью цветов"""
        if obj.pk:
            html = f"""
            <div style="display: flex; gap: 10px; margin: 10px 0;">
                <div style="width: 50px; height: 50px; background: {obj.primary_color}; border: 1px solid #ddd; border-radius: 5px;"></div>
                <div style="width: 50px; height: 50px; background: {obj.secondary_color}; border: 1px solid #ddd; border-radius: 5px;"></div>
                <div style="width: 50px; height: 50px; background: {obj.text_color}; border: 1px solid #ddd; border-radius: 5px;"></div>
                <div style="width: 50px; height: 50px; background: {obj.background_color}; border: 1px solid #ddd; border-radius: 5px;"></div>
            </div>
            <p><small>Основной | Вторичный | Текст | Фон</small></p>
            """
            return mark_safe(html)
        return "Сохраните для предпросмотра"
    color_preview.short_description = 'Превью цветов'


@admin.register(ProductFeatureConfig)
class ProductFeatureConfigAdmin(TabbedTranslationAdmin):
    list_display = ['title', 'icon', 'text', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'text']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'icon_preview']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'text', 'icon', 'icon_preview', 'order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def icon_preview(self, obj):
        """Показывает превью иконки"""
        if obj.icon:
            return format_html(
                '<i class="{}" style="font-size: 24px; color: #1976d2;"></i> <span style="margin-left: 10px;">{}</span>',
                obj.icon, obj.icon
            )
        return "Иконка не указана"
    icon_preview.short_description = 'Превью иконки'


@admin.register(TelegramConfig)
class TelegramConfigAdmin(admin.ModelAdmin):
    # def has_module_permission(self, request):
    #     """Скрываем из списка админки, но оставляем доступ к редактированию"""
    #     return False
    
    list_display = ['is_active', 'notify_new_orders', 'notify_status_changes', 'notify_contact_messages', 'bot_token_preview', 'group_chat_id', 'updated_at']
    readonly_fields = ['updated_at', 'test_connection']
    fieldsets = (
        ('Основные настройки', {
            'fields': ('is_active', 'bot_token', 'group_chat_id'),
            'description': 'Для получения токена бота обратитесь к @BotFather в Telegram. Для получения ID группы используйте бота @userinfobot или добавьте бота в группу и отправьте любое сообщение, затем используйте getUpdates API.'
        }),
        ('Типы уведомлений', {
            'fields': ('notify_new_orders', 'notify_status_changes', 'notify_contact_messages')
        }),
        ('Тестирование', {
            'fields': ('test_connection',),
            'description': 'Проверьте подключение к Telegram боту'
        }),
        ('Даты', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def bot_token_preview(self, obj):
        """Показывает частично скрытый токен"""
        if obj.bot_token:
            if len(obj.bot_token) > 20:
                return f"{obj.bot_token[:10]}...{obj.bot_token[-10:]}"
            return obj.bot_token
        return "Не указан"
    bot_token_preview.short_description = 'Токен бота'

    def test_connection(self, obj):
        """Кнопка для тестирования подключения"""
        if not obj.pk:
            return "Сохраните конфигурацию для тестирования"
        
        if not obj.bot_token or not obj.group_chat_id:
            return mark_safe(
                '<span style="color: #f44336;">⚠️ Укажите токен бота и ID группы</span>'
            )
        
        try:
            import telebot
            bot = telebot.TeleBot(obj.bot_token)
            # Пытаемся получить информацию о боте
            bot_info = bot.get_me()
            bot_name = bot_info.username if bot_info else "Неизвестно"
            
            # Пытаемся отправить тестовое сообщение
            try:
                test_message = "✅ Тестовое сообщение от Fashion Store. Бот работает корректно!"
                bot.send_message(chat_id=obj.group_chat_id, text=test_message)
                return format_html(
                    '<div style="background: #4caf50; color: white; padding: 10px; border-radius: 5px; margin: 10px 0;">'
                    '✅ <strong>Подключение успешно!</strong><br>'
                    'Бот: @{}<br>'
                    'Тестовое сообщение отправлено в группу.'
                    '</div>',
                    bot_name
                )
            except telebot.apihelper.ApiTelegramException as e:
                error_msg = str(e)
                return format_html(
                    '<div style="background: #ff9800; color: white; padding: 10px; border-radius: 5px; margin: 10px 0;">'
                    '⚠️ <strong>Бот инициализирован, но не может отправить сообщение</strong><br>'
                    'Ошибка: {}<br>'
                    'Проверьте, что бот добавлен в группу и имеет права на отправку сообщений.'
                    '</div>',
                    error_msg
                )
        except Exception as e:
            error_msg = str(e)
            return format_html(
                '<div style="background: #f44336; color: white; padding: 10px; border-radius: 5px; margin: 10px 0;">'
                '❌ <strong>Ошибка подключения</strong><br>'
                'Ошибка: {}<br>'
                'Проверьте правильность токена бота.'
                '</div>',
                error_msg
            )
    test_connection.short_description = 'Тест подключения'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject_display', 'is_read', 'created_at']
    list_filter = ['subject', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['created_at', 'updated_at', 'subject_display']
    list_editable = ['is_read']
    fieldsets = (
        ('Информация о отправителе', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Сообщение', {
            'fields': ('subject', 'subject_display', 'message', 'is_read')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subject_display(self, obj):
        return obj.get_subject_display()
    subject_display.short_description = 'Тема'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()


@admin.register(FAQ)
class FAQAdmin(TabbedTranslationAdmin):
    list_display = ('question', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'created_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('question', 'answer', 'order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')