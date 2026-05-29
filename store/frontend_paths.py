"""Пути к собранной Vite-витрине (staticfiles / collectstatic)."""
from __future__ import annotations

from pathlib import Path

from django.conf import settings


def spa_index_path() -> Path | None:
    """
    Абсолютный путь к frontend/index.html после ``npm run build``.

    - DEBUG: staticfiles finder (обычно static/frontend/), затем static/frontend/, затем STATIC_ROOT.
    - не DEBUG: только STATIC_ROOT.
    """
    if settings.DEBUG:
        from django.contrib.staticfiles import finders

        found = finders.find("frontend/index.html")
        if found:
            return Path(found)
        dev = Path(settings.BASE_DIR) / "static" / "frontend" / "index.html"
        if dev.is_file():
            return dev
        fallback = Path(settings.STATIC_ROOT) / "frontend" / "index.html"
        return fallback if fallback.is_file() else None

    prod = Path(settings.STATIC_ROOT) / "frontend" / "index.html"
    return prod if prod.is_file() else None
