from __future__ import annotations

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .context import get_current_site


class SiteFileSystemStorage(FileSystemStorage):
    """Store uploaded media inside the active site folder."""

    def __init__(self, location=None, base_url=None):
        super().__init__(location=location or self._resolve_location(), base_url=base_url or settings.MEDIA_URL)

    def _resolve_location(self) -> str:
        site = get_current_site()
        if site:
            site.media_dir.mkdir(parents=True, exist_ok=True)
            return str(site.media_dir)
        return str(settings.MEDIA_ROOT)

    def deconstruct(self):
        name, obj, args, kwargs = super().deconstruct()
        kwargs.pop('location', None)
        return name, obj, args, kwargs
