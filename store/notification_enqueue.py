"""
Enqueue Telegram notification events into the transactional outbox and schedule Celery.
"""

import logging

from django.db.transaction import on_commit

from .models import NotificationOutbox, TelegramNotificationSettings

logger = logging.getLogger(__name__)


def _schedule_outbox(outbox_id: int) -> None:
    from .tasks import process_notification_outbox

    on_commit(lambda oid=outbox_id: process_notification_outbox.delay(oid))


def enqueue_order_placed(order_id: int) -> NotificationOutbox | None:
    cfg = TelegramNotificationSettings.get_active()
    if not cfg or not cfg.is_active or not cfg.notify_new_orders:
        return None
    row = NotificationOutbox.objects.create(
        event_type=NotificationOutbox.EventType.ORDER_PLACED,
        payload={"order_id": order_id},
        status=NotificationOutbox.Status.PENDING,
    )
    _schedule_outbox(row.id)
    logger.debug("Enqueued order_placed outbox_id=%s order_id=%s", row.id, order_id)
    return row


def enqueue_order_status_changed(order_id: int, old_status: str) -> NotificationOutbox | None:
    cfg = TelegramNotificationSettings.get_active()
    if not cfg or not cfg.is_active or not cfg.notify_status_changes:
        return None
    row = NotificationOutbox.objects.create(
        event_type=NotificationOutbox.EventType.ORDER_STATUS_CHANGED,
        payload={"order_id": order_id, "old_status": old_status},
        status=NotificationOutbox.Status.PENDING,
    )
    _schedule_outbox(row.id)
    return row


def enqueue_contact_message(contact_message_id: int) -> NotificationOutbox | None:
    cfg = TelegramNotificationSettings.get_active()
    if not cfg or not cfg.is_active or not cfg.notify_contact_messages:
        return None
    row = NotificationOutbox.objects.create(
        event_type=NotificationOutbox.EventType.CONTACT_MESSAGE,
        payload={"contact_message_id": contact_message_id},
        status=NotificationOutbox.Status.PENDING,
    )
    _schedule_outbox(row.id)
    return row
