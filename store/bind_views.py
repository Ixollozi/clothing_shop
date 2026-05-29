"""
Server-to-server bind endpoint called by the central Telegram registrar after /start.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from typing import Any

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import TelegramBindIntent, TelegramSubscriber

logger = logging.getLogger(__name__)

MAX_CLOCK_SKEW_SEC = 300


def _canonical_json(data: dict[str, Any]) -> bytes:
    return json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _verify_signature(body_bytes: bytes, timestamp_header: str | None, signature_header: str | None) -> bool:
    secret = (getattr(settings, "TELEGRAM_BIND_SHARED_SECRET", None) or "").strip()
    if not secret or not timestamp_header or not signature_header:
        return False
    try:
        ts = int(timestamp_header)
    except ValueError:
        return False
    if abs(int(time.time()) - ts) > MAX_CLOCK_SKEW_SEC:
        return False
    mac = hmac.new(secret.encode("utf-8"), f"{timestamp_header}.".encode("utf-8") + body_bytes, hashlib.sha256)
    expected = mac.hexdigest()
    return hmac.compare_digest(expected, signature_header)


@csrf_exempt
@require_POST
def telegram_registrar_bind(request):
    body_bytes = request.body
    try:
        data = json.loads(body_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest("invalid json")

    if not _verify_signature(
        body_bytes,
        request.headers.get("X-Bind-Timestamp"),
        request.headers.get("X-Bind-Signature"),
    ):
        logger.warning("telegram bind: bad signature")
        return HttpResponse(status=401)

    nonce = (data.get("nonce") or "").strip()
    chat_id = data.get("telegram_chat_id")
    username = (data.get("telegram_username") or "").strip()[:255]

    if not nonce or chat_id is None:
        return HttpResponseBadRequest("missing nonce or telegram_chat_id")

    try:
        chat_id_int = int(chat_id)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("invalid telegram_chat_id")

    now = timezone.now()
    try:
        intent = TelegramBindIntent.objects.get(nonce=nonce, used_at__isnull=True)
    except TelegramBindIntent.DoesNotExist:
        logger.warning("telegram bind: unknown or used nonce")
        return HttpResponse(status=404)

    if intent.expires_at < now:
        return JsonResponse({"ok": False, "error": "expired"}, status=400)

    intent.used_at = now
    intent.save(update_fields=["used_at"])

    TelegramSubscriber.objects.update_or_create(
        telegram_chat_id=chat_id_int,
        defaults={
            "telegram_username": username,
            "display_name": username or f"chat {chat_id_int}",
            "is_active": True,
        },
    )

    logger.info("Telegram subscriber bound chat_id=%s", chat_id_int)
    return JsonResponse({"ok": True})
