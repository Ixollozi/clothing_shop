from __future__ import annotations

from django.views.static import serve

from store.platform.context import get_current_site


def site_media_serve(request, path, document_root=None):
    site = get_current_site()
    root = site.media_dir if site else document_root
    return serve(request, path, document_root=str(root))
