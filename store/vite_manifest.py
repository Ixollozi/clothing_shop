"""Чтение Vite manifest.json для подключения CSS/JS к SPA-шаблону."""
from __future__ import annotations

import json
from pathlib import Path

from django.conf import settings


def get_spa_vite_assets() -> dict[str, list[str]] | None:
    """
    Возвращает URL-пути /static/frontend/... для entry index.html.
    """
    base = Path(settings.BASE_DIR) / "static" / "frontend"
    manifest_path = base / ".vite" / "manifest.json"
    if not manifest_path.is_file():
        manifest_path = base / "manifest.json"
    if not manifest_path.is_file():
        return None
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    entry = data.get("index.html")
    if not entry:
        return None

    static_root = settings.STATIC_URL.rstrip("/")
    if not static_root.startswith("/"):
        static_root = "/" + static_root

    def to_url(rel: str) -> str:
        rel = rel.lstrip("/")
        return f"{static_root}/frontend/{rel}"

    js_urls: list[str] = []
    if entry.get("file"):
        js_urls.append(to_url(entry["file"]))
    for imp in entry.get("imports") or []:
        chunk = data.get(imp)
        if chunk and chunk.get("file"):
            u = to_url(chunk["file"])
            if u not in js_urls:
                js_urls.append(u)

    css_urls: list[str] = []
    for href in entry.get("css") or []:
        css_urls.append(to_url(href))

    return {"js": js_urls, "css": css_urls}
