from rest_framework import serializers
from .models import Category, Product, ProductImage, Cart, CartItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    discount_percent = serializers.SerializerMethodField()
    image_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'old_price',
            'category', 'category_id', 'image', 'image_url', 'image_display',
            'available_sizes', 'available_colors', 'stock', 'is_active',
            'rating', 'reviews_count', 'images', 'discount_percent', 'created_at'
        ]

    def get_discount_percent(self, obj):
        if obj.old_price and obj.old_price > obj.price:
            discount = ((obj.old_price - obj.price) / obj.old_price) * 100
            return round(discount, 0)
        return 0

    def get_image_display(self, obj):
        """Возвращает URL изображения (приоритет у image_url для внешних ссылок)"""
        if obj.image_url:
            return obj.image_url
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    total = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_id', 'quantity', 'size', 'color', 'total'
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()
    items_count = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'session_key', 'items', 'total', 'items_count', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'size', 'color', 'total']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'session_key', 'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'postal_code', 'total', 'status', 'status_display',
            'payment_method', 'payment_method_display', 'notes', 'items',
            'created_at', 'updated_at'
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'address',
            'city', 'postal_code', 'payment_method', 'notes', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        session_key = self.context['request'].session.session_key
        
        if not session_key:
            self.context['request'].session.create()
            session_key = self.context['request'].session.session_key

        validated_data['session_key'] = session_key
        
        # Подсчет общей суммы
        total = 0
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            total += product.price * item_data['quantity']

        validated_data['total'] = total
        order = Order.objects.create(**validated_data)

        # Создание элементов заказа
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price,
                size=item_data.get('size', ''),
                color=item_data.get('color', '')
            )

        return order

