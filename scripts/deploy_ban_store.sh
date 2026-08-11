#!/bin/bash
# Non-interactive deploy: ban-store.uz в†’ theme eshop on clothing platform
set -euo pipefail

PLATFORM="/var/www/platform"
SITES_ROOT="$PLATFORM/sites"
REGISTRY="$SITES_ROOT/registry.json"
DOMAIN="ban-store"
FULL_DOMAIN="ban-store.uz"
THEME="eshop"
STORE_NAME="Ban Store"
PHONE="+998(90) 000-00-00"
CITY="Tashkent"
SITE_DIR="$SITES_ROOT/$DOMAIN"
NGINX_AVAILABLE="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"
NGINX_NAME="$FULL_DOMAIN"
PLATFORM_PORT=9000

echo "=== Deploy $FULL_DOMAIN (theme=$THEME) ==="

if [ ! -d "$PLATFORM/themes/$THEME" ]; then
  echo "ERROR: theme $THEME missing in $PLATFORM/themes/"
  exit 1
fi

# 1. Pull latest code (eshop theme)
echo "--- git pull ---"
cd "$PLATFORM"
git fetch --all --prune
git pull --ff-only origin main || true
if [ ! -d "$PLATFORM/themes/$THEME" ]; then
  echo "ERROR: theme $THEME still missing after pull"
  exit 1
fi

# 2. Site folder + config.json
echo "--- site folder ---"
mkdir -p "$SITE_DIR/media"

python3 - "$SITE_DIR/config.json" "$STORE_NAME" "$FULL_DOMAIN" "$PHONE" "$CITY" <<'PY'
import json, sys
path, name, domain, phone, city = sys.argv[1:6]
cfg = {
  "store": {
    "name": name,
    "title": f"{name} - Online Store",
    "description": f"{name} store",
    "logo": "",
    "favicon": "",
  },
  "contact": {
    "phone": phone,
    "email": f"info@{domain}",
    "address": {"city": city, "street": "", "full": city},
    "working_hours": {"weekdays": "9:00 - 20:00", "weekend": "10:00 - 18:00"},
  },
  "social": {"instagram": "#", "facebook": "#", "telegram": "#", "whatsapp": "#"},
  "hero": {
    "title": "New Collection",
    "subtitle": "Discover style and comfort",
    "button_text": "View Catalog",
    "background_image": "",
  },
  "django": {
    "debug": False,
    "allowed_hosts": [domain, f"www.{domain}", "127.0.0.1", "localhost", "138.249.7.168"],
    "language_code": "ru",
    "csrf_trusted_origins": [
      f"https://{domain}",
      f"https://www.{domain}",
      f"http://{domain}",
      f"http://www.{domain}",
    ],
  },
}
with open(path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("config.json written")
PY

# 3. Seed DB from demo-eshop if available (better for demo)
if [ -f "$SITES_ROOT/demo-eshop/db.sqlite3" ] && [ ! -f "$SITE_DIR/db.sqlite3" ]; then
  echo "--- copy demo-eshop DB ---"
  cp -a "$SITES_ROOT/demo-eshop/db.sqlite3" "$SITE_DIR/db.sqlite3"
  if [ -d "$SITES_ROOT/demo-eshop/media" ]; then
    cp -a "$SITES_ROOT/demo-eshop/media/." "$SITE_DIR/media/" 2>/dev/null || true
  fi
fi

# 4. Registry: ensure theme + site entry
echo "--- registry ---"
python3 - "$REGISTRY" "$DOMAIN" "$THEME" "$STORE_NAME" "$FULL_DOMAIN" <<'PY'
import json, sys
path, slug, theme, title, domain = sys.argv[1:6]
with open(path, encoding="utf-8") as f:
    reg = json.load(f)

themes = reg.setdefault("themes", {})
if theme not in themes:
    themes[theme] = {
        "template_dirs": [f"themes/{theme}/templates"],
        "static_dirs": [f"themes/{theme}/static"],
        "locale_dirs": ["locale"],
    }
    print(f"theme {theme} added")

sites = reg.setdefault("sites", {})
sites[slug] = {
    "title": title,
    "theme": theme,
    "hosts": [domain, f"www.{domain}"],
}
with open(path, "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"site {slug} registered -> {domain} theme={theme}")
PY

# 5. Migrate + optional sample data
echo "--- migrate ---"
cd "$PLATFORM"
export PLATFORM_MODE=1
# shellcheck disable=SC1091
source "$PLATFORM/.venv/bin/activate"
python manage.py platform_migrate --site="$DOMAIN" 2>/dev/null \
  || python manage.py migrate --database="site_${DOMAIN//-/_}" 2>/dev/null \
  || true

# Try loading sample data for this site if command supports it
python manage.py load_sample_data 2>/dev/null || true

# 6. Nginx (HTTP first; SSL via certbot if DNS ok)
echo "--- nginx ---"
cat > "$NGINX_AVAILABLE/$NGINX_NAME" <<EOF
server {
    listen 80;
    server_name $FULL_DOMAIN www.$FULL_DOMAIN;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /static/ {
        proxy_pass http://127.0.0.1:$PLATFORM_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /media/ {
        proxy_pass http://127.0.0.1:$PLATFORM_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location / {
        proxy_pass http://127.0.0.1:$PLATFORM_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    client_max_body_size 10M;
    access_log /var/log/nginx/${DOMAIN}_access.log;
    error_log /var/log/nginx/${DOMAIN}_error.log;
}
EOF

ln -sfn "$NGINX_AVAILABLE/$NGINX_NAME" "$NGINX_ENABLED/$NGINX_NAME"
nginx -t
systemctl reload nginx

# 7. Restart platform
echo "--- restart platform ---"
systemctl restart platform
sleep 2
systemctl is-active platform

# 8. Local smoke test with Host header
echo "--- local smoke ---"
CODE=$(curl -s -o /tmp/ban_store_body.html -w "%{http_code}" -H "Host: $FULL_DOMAIN" http://127.0.0.1/)
echo "HTTP $CODE"
head -c 200 /tmp/ban_store_body.html; echo

# 9. Certbot only if DNS points here
MY_IP=$(curl -s --max-time 5 ifconfig.me || echo "")
DNS_IP=$(dig +short "$FULL_DOMAIN" A | head -1 | tr -d '[:space:]')
echo "Server IP: $MY_IP"
echo "DNS A $FULL_DOMAIN: $DNS_IP"

if [ -n "$DNS_IP" ] && [ "$DNS_IP" = "$MY_IP" ]; then
  echo "--- certbot ---"
  certbot --nginx -d "$FULL_DOMAIN" -d "www.$FULL_DOMAIN" --non-interactive --agree-tos --register-unsafely-without-email --redirect || true
else
  echo "SKIP certbot: DNS ($DNS_IP) != this server ($MY_IP)"
  echo "Point A-record of $FULL_DOMAIN to $MY_IP then run:"
  echo "  certbot --nginx -d $FULL_DOMAIN -d www.$FULL_DOMAIN --non-interactive --agree-tos --register-unsafely-without-email --redirect"
fi

echo "=== DONE: http://$FULL_DOMAIN/ ==="
