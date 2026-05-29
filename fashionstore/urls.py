"""
URL configuration for fashionstore project.
"""
import re
from urllib.parse import urlparse

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from store.admin_context import get_admin_index_context
from store.admin_config import unified_config_view
from store.views_spa import spa

# Кастомный индекс админки
_original_admin_index = admin.site.index


def admin_index_view(request, extra_context=None):
    extra_context = extra_context or {}
    extra_context.update(get_admin_index_context())
    return _original_admin_index(request, extra_context)


admin.site.index = admin_index_view

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "admin/config/",
        admin.site.admin_view(unified_config_view),
        name="admin_unified_config",
    ),
    path("admin/", admin.site.urls),
    path("api/", include("store.urls")),
]


def _static_media_path_prefixes():
    """Первый сегмент пути из STATIC_URL / MEDIA_URL (напр. static, media)."""
    segs = []
    for raw in (getattr(settings, "STATIC_URL", "") or "", getattr(settings, "MEDIA_URL", "") or ""):
        u = raw.strip()
        if not u:
            continue
        if "://" in u:
            path = urlparse(u).path or "/"
        else:
            path = u if u.startswith("/") else "/" + u
        parts = [p for p in path.strip("/").split("/") if p]
        if parts and parts[0] not in segs:
            segs.append(parts[0])
    return segs


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

_spa_prefix_neg = "".join(
    f"(?!{re.escape(seg)}/)" for seg in _static_media_path_prefixes()
)
urlpatterns += [re_path(rf"^{_spa_prefix_neg}.*$", spa, name="spa")]
