"""
Context processors для передачи конфигурации в шаблоны
"""
from .config_loader import get_config
from .models import Partner, Feature, Cart, ThemeConfig


def _hex_to_rgb(hex_color: str):
    if not hex_color:
        return None
    s = str(hex_color).strip()
    if not s:
        return None
    if s[0] == "#":
        s = s[1:]
    if len(s) == 3:
        s = "".join([c * 2 for c in s])
    if len(s) != 6:
        return None
    try:
        r = int(s[0:2], 16)
        g = int(s[2:4], 16)
        b = int(s[4:6], 16)
        return (r, g, b)
    except ValueError:
        return None


def _darken_hex(hex_color: str, factor: float = 0.12) -> str:
    """
    factor=0.12 -> ~12% darker.
    """
    rgb = _hex_to_rgb(hex_color)
    if not rgb:
        return hex_color
    r, g, b = rgb
    r = max(0, int(r * (1 - factor)))
    g = max(0, int(g * (1 - factor)))
    b = max(0, int(b * (1 - factor)))
    return f"#{r:02x}{g:02x}{b:02x}"


def _theme_css_vars(theme: ThemeConfig | None):
    if not theme:
        return ""
    primary = (theme.primary_color or "").strip()
    secondary = (theme.secondary_color or "").strip()
    text = (theme.text_color or "").strip()
    bg = (theme.background_color or "").strip()
    primary2 = _darken_hex(primary, 0.12) if primary else ""

    ring = ""
    rgb = _hex_to_rgb(primary)
    if rgb:
        r, g, b = rgb
        ring = f"rgba({r},{g},{b},.35)"

    # keep to the variables already used in styles.css
    parts = []
    if bg:
        parts.append(f"--bg0:{bg};")
        parts.append(f"--bg1:{bg};")
        parts.append(f"--card:{'#ffffff' if bg.lower() != '#ffffff' else '#ffffff'};")
        bg_rgb = _hex_to_rgb(bg)
        if bg_rgb:
            br, bgc, bb = bg_rgb
            parts.append(f"--bg-rgb:{br},{bgc},{bb};")
    if text:
        parts.append(f"--text:{text};")
        text_rgb = _hex_to_rgb(text)
        if text_rgb:
            tr, tg, tb = text_rgb
            parts.append(f"--text-rgb:{tr},{tg},{tb};")
            parts.append(f"--muted:rgba({tr},{tg},{tb},.62);")
            parts.append(f"--border:rgba({tr},{tg},{tb},.12);")
    if primary:
        parts.append(f"--primary:{primary};")
        parts.append(f"--wood:{primary};")
    if rgb:
        r, g, b = rgb
        parts.append(f"--primary-rgb:{r},{g},{b};")
    if primary2:
        parts.append(f"--primary2:{primary2};")
    if secondary:
        parts.append(f"--secondary:{secondary};")
        secondary_rgb = _hex_to_rgb(secondary)
        if secondary_rgb:
            sr, sg, sb = secondary_rgb
            parts.append(f"--secondary-rgb:{sr},{sg},{sb};")
            parts.append(f"--ring-secondary:rgba({sr},{sg},{sb},.22);")
    if ring:
        parts.append(f"--ring:{ring};")
    return " ".join(parts)


def store_config(request):
    """
    Передает конфигурацию магазина во все шаблоны
    """
    config = get_config()
    # Получаем партнеров из БД вместо конфига
    partners = Partner.objects.filter(is_active=True).order_by('order', 'name')
    # Получаем features из БД вместо конфига
    features = Feature.objects.filter(is_active=True).order_by('order', 'title')
    
    # Cart badge count (header)
    cart_items_count = 0
    try:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()
        if cart:
            cart_items_count = cart.items_count
    except Exception:
        cart_items_count = 0

    active_theme = None
    try:
        active_theme = ThemeConfig.objects.filter(is_active=True).first()
    except Exception:
        active_theme = None

    return {
        'store_config': config,
        'store_name': config.get('store', {}).get('name', 'Fashion Store'),
        'store_title': config.get('store', {}).get('title', 'Fashion Store'),
        'store_description': config.get('store', {}).get('description', ''),
        'contact_info': config.get('contact', {}),
        'social_links': config.get('social', {}),
        'partners': partners,  # Теперь из БД
        'features': features,  # Теперь из БД
        'about_info': config.get('about', {}),
        'hero_config': config.get('hero', {}),
        'seo_config': config.get('seo', {}),
        'theme_config': config.get('theme', {}),
        'active_theme': active_theme,
        'theme_css_vars': _theme_css_vars(active_theme),
        'cart_items_count': cart_items_count,
    }

