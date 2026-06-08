from pathlib import Path

from config.env import ENV_FILE, env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env("SECRET_KEY", default="dev-insecure-secret-key")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

INSTALLED_APPS = [
    "daphne",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "django_q",
    "channels",
    "apps.core",
    "apps.identity",
    "apps.audit",
    "apps.transactions",
    "apps.rules",
    "apps.alerts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "apps.core.middleware.RequestContextMiddleware",
]

ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": env.db("DATABASE_URL", default="postgres://smartcomply:smartcomply@localhost:5432/smartcomply")
}

REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CHANNEL_REDIS_URL = env("CHANNEL_REDIS_URL", default="redis://localhost:6379/1")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                {
                    "address": CHANNEL_REDIS_URL,
                    # channels_redis polls with 5s bzpopmin; default redis-py socket_timeout
                    # is also 5s and races, dropping idle WebSockets with code 1011.
                    "socket_timeout": None,
                    "socket_connect_timeout": 5,
                    "socket_keepalive": True,
                    "health_check_interval": 30,
                    "retry_on_timeout": True,
                }
            ],
        },
    }
}

Q_CLUSTER = {
    "name": "smartcomply",
    "workers": 2,
    "recycle": 500,
    "timeout": 60,
    "retry": 120,
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",
    "redis": REDIS_URL,
    "sync": env.bool("Q_CLUSTER_SYNC", default=False),
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.identity.authentication.APIKeyAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "SmartComply Transaction Monitoring API",
    "VERSION": "1.0.0",
    "DESCRIPTION": "Transaction monitoring API. Authenticate with the X-API-Key header.",
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key",
            }
        }
    },
    "SECURITY": [{"ApiKeyAuth": []}],
}

BOOTSTRAP_API_KEY = env("BOOTSTRAP_API_KEY", default="sc_bootstrap_dev_key_change_me")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
}
