"""
Celery tasks: drain notification outbox and send to Telegram Bot API.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import telebot
from celery import shared_task
from django.db import transaction

from .models import ContactMessage, NotificationOutbox, Order, TelegramNotificationSettings, TelegramSubscriber
from .telegram_messages import (
    format_contact_message,
    format_new_order_message,
    format_status_change_message,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 8


def _reschedule(outbox_id: int, attempts: int) -> None:
    delay = min(300, 10 * (2 ** min(attempts, 5)))
    process_notification_outbox.apply_async(args=[outbox_id], countdown=delay)


@shared_task
def process_notification_outbox(outbox_id: int) -> None:
    try:
        with transaction.atomic():
            row = NotificationOutbox.objects.select_for_update().get(pk=outbox_id)
            if row.status != NotificationOutbox.Status.PENDING:
                return
            row.status = NotificationOutbox.Status.PROCESSING
            row.save(update_fields=["status", "updated_at"])
    except NotificationOutbox.DoesNotExist:
        logger.warning("Outbox row missing id=%s", outbox_id)
        return

    cfg = TelegramNotificationSettings.get_active()
    token = cfg.resolved_bot_token() if cfg else ""

    def _fail_or_retry(msg: str) -> None:
        with transaction.atomic():
            row = NotificationOutbox.objects.select_for_update().get(pk=outbox_id)
            row.attempts += 1
            row.last_error = msg[:2000]
            if row.attempts >= MAX_ATTEMPTS:
                row.status = NotificationOutbox.Status.FAILED
            else:
                row.status = NotificationOutbox.Status.PENDING
            row.save(update_fields=["attempts", "last_error", "status", "updated_at"])
            attempts = row.attempts
            is_failed = row.status == NotificationOutbox.Status.FAILED
        if not is_failed:
            _reschedule(outbox_id, attempts)
        else:
            logger.error("Outbox id=%s failed permanently: %s", outbox_id, msg)

    def _mark_sent(note: str = "") -> None:
        NotificationOutbox.objects.filter(pk=outbox_id).update(
            status=NotificationOutbox.Status.SENT,
            last_error=note[:2000],
        )

    if not cfg or not cfg.is_active:
        _mark_sent("skipped: channel inactive")
        return

    if not token:
        _fail_or_retry("Нет токена бота: укажите «Токен бота» в настройках Telegram или TELEGRAM_BOT_TOKEN в окружении.")
        return

    subscribers = list(TelegramSubscriber.objects.filter(is_active=True))
    if not subscribers:
        _mark_sent("skipped: no active subscribers")
        return

    try:
        text, allowed = _build_message(row)
    except Exception as e:
        logger.exception("Outbox id=%s build message error", outbox_id)
        _fail_or_retry(f"build: {e}")
        return

    if not allowed:
        _mark_sent("skipped: notification type disabled")
        return

    bot = telebot.TeleBot(token)
    try:
        for sub in subscribers:
            bot.send_message(chat_id=sub.telegram_chat_id, text=text, parse_mode="HTML")
    except telebot.apihelper.ApiTelegramException as e:
        logger.warning("Telegram API error outbox=%s: %s", outbox_id, e)
        _fail_or_retry(f"telegram: {e}")
        return
    except Exception as e:
        logger.exception("Unexpected send error outbox=%s", outbox_id)
        _fail_or_retry(f"send: {e}")
        return

    _mark_sent("")
    logger.info("Outbox id=%s delivered to %s chats", outbox_id, len(subscribers))


def _build_message(row: NotificationOutbox) -> tuple[str, bool]:
    """Returns (html_text, allowed)."""
    if row.event_type == NotificationOutbox.EventType.ORDER_PLACED:
        oid = row.payload.get("order_id")
        order = Order.objects.prefetch_related("items__product").get(pk=oid)
        return format_new_order_message(order), True

    if row.event_type == NotificationOutbox.EventType.ORDER_STATUS_CHANGED:
        oid = row.payload.get("order_id")
        old_status = row.payload.get("old_status")
        order = Order.objects.prefetch_related("items__product").get(pk=oid)
        return format_status_change_message(order, old_status), True

    if row.event_type == NotificationOutbox.EventType.CONTACT_MESSAGE:
        cid = row.payload.get("contact_message_id")
        contact = ContactMessage.objects.get(pk=cid)
        return format_contact_message(contact), True

    return "", False
