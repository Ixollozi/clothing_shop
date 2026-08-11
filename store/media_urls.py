"""Display URL helpers for products and categories (upload > URL > gallery)."""
from __future__ import annotations


def _safe_file_url(file_field) -> str:
    if not file_field:
        return ""
    try:
        name = getattr(file_field, "name", None)
        if not name:
            return ""
        return file_field.url or ""
    except Exception:
        return ""


def product_display_image_url(product) -> str:
    """
    Best card/primary image URL for a product.
    Priority: uploaded primary → first ProductImage → external URL.
    (External URL is last so demo Unsplash links don't hide real uploads.)
    """
    if product is None:
        return ""

    url = _safe_file_url(getattr(product, "image", None))
    if url:
        return url

    images = getattr(product, "images", None)
    if images is not None:
        try:
            iterable = images.all() if hasattr(images, "all") else images
            for img in iterable:
                url = _safe_file_url(getattr(img, "image", None))
                if url:
                    return url
        except Exception:
            pass

    return (getattr(product, "image_url", None) or "").strip()


def category_display_image_url(category) -> str:
    if category is None:
        return ""
    if isinstance(category, dict):
        return (category.get("image_url") or category.get("image") or "") or ""
    url = _safe_file_url(getattr(category, "image", None))
    if url:
        return url
    return (getattr(category, "image_url", None) or "").strip()


def product_gallery_urls(product) -> list[str]:
    """Ordered unique gallery URLs: primary file + extras + external URL last."""
    seen: set[str] = set()
    out: list[str] = []

    def add(url: str) -> None:
        url = (url or "").strip()
        if not url or url in seen:
            return
        seen.add(url)
        out.append(url)

    if product is None:
        return out

    add(_safe_file_url(getattr(product, "image", None)))

    images = getattr(product, "images", None)
    if images is not None:
        try:
            iterable = images.all() if hasattr(images, "all") else images
            for img in iterable:
                add(_safe_file_url(getattr(img, "image", None)))
        except Exception:
            pass

    add(getattr(product, "image_url", None) or "")
    return out
