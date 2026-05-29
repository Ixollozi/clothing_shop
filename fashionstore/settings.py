"""
Django settings for fashionstore project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем настройки Django из config.json
try:
    from store.config_loader import get_django_config
    DJANGO_CONFIG = get_django_config()
except ImportError:
    # Если импорт не удался (например, при миграциях), используем значения по умолчанию
    DJANGO_CONFIG = {}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Можно переопределить через config.json, но рекомендуется использовать переменные окружения в продакшене
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or DJANGO_CONFIG.get('secret_key', 'django-insecure-your-secret-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# Можно переопределить через config.json
DEBUG = os.environ.get('DJANGO_DEBUG', '').lower() in ('true', '1', 'yes') or DJANGO_CONFIG.get('debug', True)

# ALLOWED_HOSTS можно настроить через config.json
ALLOWED_HOSTS = DJANGO_CONFIG.get('allowed_hosts', ['*'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Для форматирования чисел
    'rest_framework',
    'corsheaders',
    'modeltranslation',  # Должен быть перед 'store'
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # LocaleMiddleware сразу после Session: язык из cookie (set_language) читается на каждом запросе
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fashionstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # Для i18n
                'store.context_processors.store_config',  # Конфигурация магазина
            ],
        },
    },
]

WSGI_APPLICATION = 'fashionstore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Настройки БД можно переопределить через config.json
db_config = DJANGO_CONFIG.get('database', {})
DATABASES = {
    'default': {
        'ENGINE': db_config.get('engine', 'django.db.backends.sqlite3'),
        'NAME': BASE_DIR / db_config.get('name', 'db.sqlite3'),
    }
}

# Если указаны дополнительные параметры для БД (PostgreSQL, MySQL и т.д.)
if db_config.get('user'):
    DATABASES['default']['USER'] = db_config.get('user')
if db_config.get('password'):
    DATABASES['default']['PASSWORD'] = db_config.get('password')
if db_config.get('host'):
    DATABASES['default']['HOST'] = db_config.get('host')
if db_config.get('port'):
    DATABASES['default']['PORT'] = db_config.get('port')


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# Настройки языка и времени можно переопределить через config.json
LANGUAGE_CODE = DJANGO_CONFIG.get('language_code', 'ru')

# Маппинг языков для LANGUAGES
LANGUAGE_NAMES = {
    'ru': 'Русский',
    'en': 'English',
    'uz': 'O\'zbek',
}

# Получаем языки из config.json или используем по умолчанию
languages_config = DJANGO_CONFIG.get('languages', ['ru', 'en', 'uz'])
LANGUAGES = [(lang, LANGUAGE_NAMES.get(lang, lang.capitalize())) for lang in languages_config]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = DJANGO_CONFIG.get('time_zone', 'Asia/Tashkent')

USE_I18N = True
USE_L10N = True

USE_TZ = True

# Язык после POST /i18n/setlang/ хранится в cookie (Django 5.x), не в сессии
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_HTTPONLY = False
LANGUAGE_COOKIE_SECURE = False
LANGUAGE_COOKIE_SAMESITE = 'Lax'

# Session settings для сохранения языка
# Можно переопределить через config.json
session_config = DJANGO_CONFIG.get('session', {})
SESSION_COOKIE_AGE = session_config.get('cookie_age', 86400)  # 24 часа
SESSION_COOKIE_HTTPONLY = session_config.get('cookie_httponly', True)
SESSION_COOKIE_SECURE = session_config.get('cookie_secure', False)  # True для HTTPS в продакшене
SESSION_SAVE_EVERY_REQUEST = session_config.get('save_every_request', True)  # Сохранять сессию при каждом запросе

# Modeltranslation settings
# Используем языки из config.json
MODELTRANSLATION_DEFAULT_LANGUAGE = DJANGO_CONFIG.get('default_language', 'ru')
MODELTRANSLATION_LANGUAGES = tuple(languages_config)
MODELTRANSLATION_FALLBACK_LANGUAGES = tuple(languages_config)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Настройки статических файлов можно переопределить через config.json
static_config = DJANGO_CONFIG.get('static', {})
STATIC_URL = static_config.get('url', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, static_config.get('root', 'staticfiles'))

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Исходники Vite/React (`frontend/`) и лимит товаров в bootstrap
_frontend_cfg = DJANGO_CONFIG.get('frontend')
if not isinstance(_frontend_cfg, dict):
    _frontend_cfg = {}
FRONTEND_SOURCE_ROOT = BASE_DIR / _frontend_cfg.get('source_dir', 'frontend')
SPA_BOOTSTRAP_PRODUCT_LIMIT = int(_frontend_cfg.get('bootstrap_product_limit', 500))
# Поле Product.price в БД — в «малых» единицах; на витрине умножаем до сум (UZS), см. bootstrap priceUzsMultiplier
SPA_PRICE_UZS_MULTIPLIER = int(_frontend_cfg.get('price_uzs_multiplier', DJANGO_CONFIG.get('price_uzs_multiplier', 10000)))

# Кодировка ответов и шаблонов (кириллица)
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

# Настройки медиа файлов можно переопределить через config.json
media_config = DJANGO_CONFIG.get('media', {})
MEDIA_URL = media_config.get('url', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, media_config.get('root', 'media'))

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
# Можно переопределить через config.json
rest_config = DJANGO_CONFIG.get('rest_framework', {})
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': rest_config.get('page_size', 12),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# CORS settings
# Можно переопределить через config.json
cors_config = DJANGO_CONFIG.get('cors', {})
CORS_ALLOWED_ORIGINS = cors_config.get('allowed_origins', [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
])

CORS_ALLOW_ALL_ORIGINS = cors_config.get('allow_all_origins', True)  # Для разработки, в продакшене убрать

CORS_ALLOW_CREDENTIALS = cors_config.get('allow_credentials', True)

# CSRF settings
# Можно переопределить через config.json
csrf_origins = DJANGO_CONFIG.get('csrf_trusted_origins', [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
])
# Фильтруем "*" так как Django 4.0+ требует полные URL с протоколом
CSRF_TRUSTED_ORIGINS = [origin for origin in csrf_origins if origin != "*"]
# Если в конфиге только "*", список станет пустым — добавляем типичные dev-оригины (в т.ч. порт 8001)
if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = [
        'http://127.0.0.1:8000',
        'http://127.0.0.1:8001',
        'http://127.0.0.1:8002',
        'http://localhost:8000',
        'http://localhost:8001',
        'http://localhost:8002',
        'http://127.0.0.1:5500',
        'http://localhost:5500',
    ]

# Email settings
# Можно переопределить через config.json
email_config = DJANGO_CONFIG.get('email', {})
EMAIL_BACKEND = email_config.get('backend', 'django.core.mail.backends.console.EmailBackend')
if email_config.get('host'):
    EMAIL_HOST = email_config.get('host')
if email_config.get('port'):
    EMAIL_PORT = email_config.get('port')
EMAIL_USE_TLS = email_config.get('use_tls', True)
EMAIL_USE_SSL = email_config.get('use_ssl', False)
if email_config.get('username'):
    EMAIL_HOST_USER = email_config.get('username')
if email_config.get('password'):
    EMAIL_HOST_PASSWORD = email_config.get('password')
EMAIL_FROM = email_config.get('from_email', 'noreply@fashionstore.ru')


# --- Celery ---
# Прод: Redis + отдельный процесс `celery -A fashionstore worker`.
# Локально (DEBUG=True): по умолчанию задачи выполняются в процессе Django — Redis и worker не обязательны.
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_EAGER_PROPAGATES = True

_eager_env = os.environ.get('CELERY_TASK_ALWAYS_EAGER', '').strip().lower()
if _eager_env in ('true', '1', 'yes'):
    CELERY_TASK_ALWAYS_EAGER = True
elif _eager_env in ('false', '0', 'no'):
    CELERY_TASK_ALWAYS_EAGER = False
else:
    CELERY_TASK_ALWAYS_EAGER = bool(DEBUG)

if CELERY_TASK_ALWAYS_EAGER:
    # Без Redis: in-memory broker + backend, иначе даже при eager Celery тянет Redis и падает.
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'memory://')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'cache+memory://')
else:
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', CELERY_BROKER_URL)

# --- Telegram: shared bot token (env), per-site subscribers in DB ---
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_BOT_USERNAME = os.environ.get('TELEGRAM_BOT_USERNAME', '').lstrip('@')
SITE_TELEGRAM_CODE = os.environ.get('SITE_TELEGRAM_CODE', '').strip()
SITE_PUBLIC_URL = os.environ.get('SITE_PUBLIC_URL', '').rstrip('/')
TELEGRAM_BIND_SHARED_SECRET = os.environ.get('TELEGRAM_BIND_SHARED_SECRET', '')
