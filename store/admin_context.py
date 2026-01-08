"""
Контекст для кастомного индекса админки
"""
from django.db.models import Sum
from .models import Product, Order, Category, Cart, Partner


def get_admin_index_context():
    """Возвращает контекст для кастомного индекса админки"""
    return {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'total_categories': Category.objects.count(),
        'total_carts': Cart.objects.count(),
        'total_partners': Partner.objects.count(),
        'active_partners': Partner.objects.filter(is_active=True).count(),
        'latest_orders': Order.objects.select_related().order_by('-created_at')[:5],
        'latest_products': Product.objects.select_related('category').order_by('-created_at')[:5],
        'latest_partners': Partner.objects.order_by('-created_at')[:5],
        'pending_orders': Order.objects.filter(status='pending').count(),
        'processing_orders': Order.objects.filter(status='processing').count(),
        'delivered_orders': Order.objects.filter(status='delivered').count(),
        'cancelled_orders': Order.objects.filter(status='cancelled').count(),
        'total_revenue': f"{Order.objects.filter(status__in=['delivered', 'shipped', 'processing']).aggregate(total=Sum('total'))['total'] or 0:.2f}",
    }


