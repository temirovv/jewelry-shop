import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me-in-production")

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

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
]

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

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.users.authentication.TelegramAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# CORS
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173"
).split(",")
CORS_ALLOW_CREDENTIALS = True
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
]

# Development uchun barcha origin larga ruxsat
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", TELEGRAM_BOT_TOKEN)  # Notification uchun
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# Unfold Admin Configuration
UNFOLD = {
    "SITE_TITLE": "Jewelry Shop",
    "SITE_HEADER": "Jewelry Shop Admin",
    "SITE_SUBHEADER": "Premium Zargarlik Do'koni",
    "SITE_DROPDOWN": [
        {
            "icon": "storefront",
            "title": "Saytga o'tish",
            "link": "/",
        },
    ],
    "SITE_SYMBOL": "diamond",
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
                ],
            },
            {
                "title": "Katalog",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Mahsulotlar",
                        "icon": "diamond",
                        "link": "/admin/products/product/",
                        "badge": "apps.products.utils.get_products_count",
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
