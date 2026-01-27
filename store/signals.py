"""
Сигналы Django для отправки уведомлений в Telegram
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Order)
def save_old_status(sender, instance, **kwargs):
    """Сохраняет старый статус заказа перед сохранением"""
    if instance.pk:
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Order)
def notify_order_status_change(sender, instance, created, **kwargs):
    """Отправляет уведомление в Telegram при изменении статуса заказа"""
    if created:
        # Новый заказ - уведомление уже отправлено в сериализаторе
        return
    
    # Проверяем, изменился ли статус
    old_status = getattr(instance, '_old_status', None)
    if old_status and old_status != instance.status:
        try:
            from .telegram_notifier import telegram_notifier
            telegram_notifier.notify_status_change(instance, old_status=old_status)
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления об изменении статуса в Telegram: {e}")
