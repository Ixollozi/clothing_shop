"""
URL configuration for fashionstore project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.admin_context import get_admin_index_context
from store.views_frontend import (
    index, catalog, product_detail, cart, about, contact, delivery
)
from store.admin_config import unified_config_view


# Кастомный индекс админки - сохраняем оригинальный метод
_original_admin_index = admin.site.index

def admin_index_view(request, extra_context=None):
    extra_context = extra_context or {}
    extra_context.update(get_admin_index_context())
    # Вызываем оригинальный метод, а не переопределенный
    return _original_admin_index(request, extra_context)

admin.site.index = admin_index_view

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/config/', admin.site.admin_view(unified_config_view), name='admin_unified_config'),
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),  # API endpoints
    # Frontend pages
    path('', index, name='index'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<slug:slug>/', product_detail, name='product'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('delivery/', delivery, name='delivery'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


