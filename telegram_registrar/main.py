"""
Central Telegram webhook: one Bot API webhook for all shops.
Configure TELEGRAM_REGISTRAR_SITES_JSON mapping SITE_TELEGRAM_CODE -> base_url + bind_secret.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import time
from typing import Any

import httpx
from fastapi import FastAPI, Header, HTTPException, Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("registrar")

app = FastAPI(title="Telegram bind registrar")

WEBHOOK_SECRET = (os.environ.get("TELEGRAM_WEBHOOK_SECRET") or "").strip()
SITES_RAW = os.environ.get("TELEGRAM_REGISTRAR_SITES_JSON", "{}")
BOT_TOKEN = (os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()


def _load_sites() -> dict[str, dict[str, str]]:
    try:
        data = json.loads(SITES_RAW)
    except json.JSONDecodeError as e:
        logger.error("Invalid TELEGRAM_REGISTRAR_SITES_JSON: %s", e)
        return {}
    if not isinstance(data, dict):
        return {}
    out: dict[str, dict[str, str]] = {}
    for code, cfg in data.items():
        if isinstance(cfg, dict) and "base_url" in cfg and "bind_secret" in cfg:
            out[str(code)] = {"base_url": str(cfg["base_url"]), "bind_secret": str(cfg["bind_secret"])}
    return out


async def _telegram_send_message(chat_id: int, text: str) -> None:
    if not BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not set; cannot reply with chat_id")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})
        if r.status_code >= 400:
            logger.warning("sendMessage failed: %s %s", r.status_code, r.text[:300])


def _sign(secret: str, body: dict[str, Any]) -> tuple[str, str, bytes]:
    body_bytes = json.dumps(body, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ts = str(int(time.time()))
    sig = hmac.new(secret.encode("utf-8"), f"{ts}.".encode("utf-8") + body_bytes, hashlib.sha256).hexdigest()
    return ts, sig, body_bytes


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
    secret_token: str | None = Header(default=None, alias="X-Telegram-Bot-Api-Secret-Token"),
) -> dict[str, bool]:
    if WEBHOOK_SECRET and (secret_token or "") != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="invalid webhook secret")

    data = await request.json()
    msg = data.get("message") or {}
    text = (msg.get("text") or "").strip()
    chat = msg.get("chat") or {}
    user = msg.get("from") or {}
    chat_id = chat.get("id")
    username = (user.get("username") or "") or ""

    if not text.startswith("/start"):
        return {"ok": True}

    parts = text.split(maxsplit=1)
    payload = parts[1].strip() if len(parts) > 1 else ""
    if "_" not in payload:
        # Просто /start или параметр без привязки к магазину — отправляем chat_id владельцу
        if chat_id is not None:
            hint = (
                "Ваш <b>chat_id</b> для уведомлений в админке магазина "
                "(раздел «Telegram — кому слать»):\n\n"
                f"<code>{chat_id}</code>"
            )
            try:
                await _telegram_send_message(int(chat_id), hint)
            except Exception as e:
                logger.exception("chat_id reply failed: %s", e)
        return {"ok": True}

    site_code, nonce = payload.split("_", 1)
    site_code = site_code.strip()
    nonce = nonce.strip()
    sites = _load_sites()
    site = sites.get(site_code)
    if not site or chat_id is None:
        logger.info("Unknown site_code=%s or missing chat_id", site_code)
        return {"ok": True}

    base = site["base_url"].rstrip("/")
    secret = site["bind_secret"]
    body = {"nonce": nonce, "telegram_chat_id": chat_id, "telegram_username": username}
    ts, sig, body_bytes = _sign(secret, body)
    url = f"{base}/api/internal/telegram-bind/"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                url,
                content=body_bytes,
                headers={
                    "Content-Type": "application/json",
                    "X-Bind-Timestamp": ts,
                    "X-Bind-Signature": sig,
                },
            )
    except httpx.RequestError as e:
        logger.exception("Bind callback failed: %s", e)
        return {"ok": True}

    if r.status_code >= 400:
        logger.warning("Shop bind returned %s: %s", r.status_code, r.text[:500])
    else:
        logger.info("Bound site_code=%s chat_id=%s", site_code, chat_id)
    return {"ok": True}
