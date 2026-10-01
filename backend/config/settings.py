import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

# Standart qiymat False: env yo'qolsa ham prod "fail-open" bo'lib, DEBUG
# mock user (autentifikatsiyasiz kirish) yoqilib qolmasin.
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-dev-only-key-do-not-use-in-production"
    else:
        raise RuntimeError("SECRET_KEY environment variable must be set in production")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Application definition
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "corsheaders",
    "django_filters",
    "import_export",
    # Local apps
    "apps.users",
    "apps.products",
    "apps.orders",
    "apps.cart",
    "apps.delivery",
    # Oxirida bo'lishi kerak (django-axes talabi)
    "axes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Admin login'ga brute-force himoyasi: bitta IP'dan 5 ta xato urinishdan
# keyin 1 soatga blok. Urinishlar DB'da — barcha gunicorn worker'lar uchun umumiy.
# Blokni qo'lda ochish: python manage.py axes_reset_ip <ip>
AXES_FAILURE_LIMIT = int(os.getenv("AXES_FAILURE_LIMIT", "5"))
AXES_COOLOFF_TIME = 1  # soat
AXES_LOCKOUT_PARAMETERS = ["ip_address"]
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_TEMPLATE = "admin/lockout.html"
# Docker nginx'ga hamma so'rov host nginx'dan keladi, ya'ni REMOTE_ADDR doim
# bir xil — u bo'yicha bloklash hammani birdan bloklab qo'yardi. Mijoz IP'si
# X-Forwarded-For'dan olinadi. ipware'da proxy_count DRF'ning NUM_PROXIES'idan
# farqli hisoblanadi: "mijoz, host-nginx" zanjiri uchun to'g'ri qiymat 1
# (soxta XFF qo'shilsa ham haqiqiy IP olinadi — test_axes.py da tekshirilgan).
AXES_IPWARE_META_PRECEDENCE_ORDER = ("HTTP_X_FORWARDED_FOR", "REMOTE_ADDR")
AXES_IPWARE_PROXY_COUNT = int(os.getenv("AXES_IPWARE_PROXY_COUNT", "1"))
# Test client.login() request bermaydi, axes esa uni talab qiladi.
# Axes'ning o'z testlari uni override_settings bilan yoqadi.
AXES_ENABLED = not TESTING

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# Development: SQLite, Production: PostgreSQL
if os.getenv("DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Reverse proxy (nginx) TLS'ni tugatadi va X-Forwarded-Proto yuboradi.
# Busiz Django so'rovni HTTP deb biladi va build_absolute_uri() rasm/fayl
# URL'larini http:// bilan yasaydi — HTTPS sahifada ular mixed content
# sifatida bloklanadi.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False

# Throttle hisoblagichlari keshda turadi. Testlarda ular testdan testga
# o'tib, bir-biriga bog'liq bo'lmagan testlarni 429 bilan yiqitmasin —
# throttle testlari LocMem keshni o'zlari yoqadi.
if TESTING:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.users.authentication.TelegramAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
        # Har bir buyurtma barcha adminlarga Telegram xabar yuboradi —
        # spam bilan admin chatini to'ldirib yuborishning oldini olish
        "orders": os.getenv("ORDERS_THROTTLE_RATE", "10/hour"),
    },
    # So'rov ikki proxy'dan o'tadi: host nginx -> docker nginx -> gunicorn.
    # Busiz DRF X-Forwarded-For'ni butunlay IP deb oladi va mijoz soxta
    # header yuborib throttle'ni aylanib o'ta oladi.
    "NUM_PROXIES": int(os.getenv("NUM_PROXIES", "2")),
}

# CORS
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173"
).split(",")
CORS_ALLOW_CREDENTIALS = True

# CSRF
CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost:3000,http://localhost:5173"
).split(",")
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-telegram-init-data",
    "x-bot-token",
    "x-telegram-user-id",
]

# Development uchun localhost origin larga ruxsat
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", TELEGRAM_BOT_TOKEN)  # Notification uchun
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# Unfold Admin Configuration
UNFOLD = {
    "SITE_TITLE": "Ziyora",
    "SITE_HEADER": "Ziyora Admin",
    "SITE_SUBHEADER": "Kosmetika Marketplace",
    "SITE_DROPDOWN": [
        {
            "icon": "storefront",
            "title": "Saytga o'tish",
            "link": "/",
        },
    ],
    "SITE_SYMBOL": "spa",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "config.settings.environment_callback",
    "DASHBOARD_CALLBACK": "config.dashboard.get_dashboard_callback",
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
        },
        "primary": {
            "50": "255 251 235",
            "100": "254 243 199",
            "200": "253 230 138",
            "300": "252 211 77",
            "400": "251 191 36",
            "500": "245 158 11",
            "600": "217 119 6",
            "700": "180 83 9",
            "800": "146 64 14",
            "900": "120 53 15",
            "950": "69 26 3",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Boshqaruv",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": "/admin/",
                    },
                    {
                        "title": "Moliyaviy hisobot",
                        "icon": "monitoring",
                        "link": "/admin/hisobot/",
                    },
                ],
            },
            {
                "title": "Katalog",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Mahsulotlar",
                        "icon": "spa",
                        "link": "/admin/products/product/",
                        "badge": "apps.products.utils.get_products_count",
                    },
                    {
                        "title": "Brendlar",
                        "icon": "loyalty",
                        "link": "/admin/products/brand/",
                    },
                    {
                        "title": "Kategoriyalar",
                        "icon": "category",
                        "link": "/admin/products/category/",
                    },
                    {
                        "title": "Bannerlar",
                        "icon": "view_carousel",
                        "link": "/admin/products/banner/",
                    },
                ],
            },
            {
                "title": "Savdo",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Buyurtmalar",
                        "icon": "shopping_cart",
                        "link": "/admin/orders/order/",
                        "badge": "apps.orders.utils.get_pending_orders_count",
                    },
                    {
                        "title": "Savatlar",
                        "icon": "shopping_bag",
                        "link": "/admin/cart/cart/",
                    },
                    {
                        "title": "Viloyatlar",
                        "icon": "map",
                        "link": "/admin/delivery/region/",
                    },
                    {
                        "title": "Yetkazish zonalari",
                        "icon": "local_shipping",
                        "link": "/admin/delivery/deliveryzone/",
                    },
                ],
            },
            {
                "title": "Foydalanuvchilar",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Telegram Users",
                        "icon": "group",
                        "link": "/admin/users/telegramuser/",
                        "badge": "apps.users.utils.get_users_count",
                    },
                    {
                        "title": "Sevimlilar",
                        "icon": "favorite",
                        "link": "/admin/users/favorite/",
                    },
                    {
                        "title": "Admin Users",
                        "icon": "admin_panel_settings",
                        "link": "/admin/auth/user/",
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": ["products.product"],
            "items": [
                {
                    "title": "Barchasi",
                    "link": "/admin/products/product/",
                },
                {
                    "title": "Sotuvda",
                    "link": "/admin/products/product/?in_stock=1",
                },
                {
                    "title": "Maxsus",
                    "link": "/admin/products/product/?is_featured=1",
                },
            ],
        },
        {
            "models": ["orders.order"],
            "items": [
                {
                    "title": "Barchasi",
                    "link": "/admin/orders/order/",
                },
                {
                    "title": "Kutilmoqda",
                    "link": "/admin/orders/order/?status=pending",
                },
                {
                    "title": "Tasdiqlangan",
                    "link": "/admin/orders/order/?status=confirmed",
                },
                {
                    "title": "Jarayonda",
                    "link": "/admin/orders/order/?status=processing",
                },
                {
                    "title": "Yetkazilgan",
                    "link": "/admin/orders/order/?status=delivered",
                },
                {
                    "title": "Bekor qilingan",
                    "link": "/admin/orders/order/?status=cancelled",
                },
            ],
        },
    ],
}


def environment_callback(request):
    """Return environment name and color."""
    if DEBUG:
        return ["Development", "warning"]
    return ["Production", "success"]
