from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, CartViewSet, OrderViewSet, submit_contact_message
from .views_frontend import (
    index, catalog, product_detail, cart, about, contact, delivery, faq
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

# API URLs - только для /api/
api_urlpatterns = [
    path('', include(router.urls)),
    path('contact/submit/', submit_contact_message, name='submit_contact_message'),
]

# Frontend URLs - только для корня
frontend_urlpatterns = [
    path('', index, name='index'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<slug:slug>/', product_detail, name='product'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('delivery/', delivery, name='delivery'),
    path('faq/', faq, name='faq'),
]

# По умолчанию возвращаем API URLs (для /api/)
urlpatterns = api_urlpatterns
