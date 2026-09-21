"""
Django settings for the portfolio project.

Local development:
- SQLite
- DEBUG enabled by default
- Normal static file storage

Production:
- Vercel
- Environment variables
- WhiteNoise for static files
- Optional PostgreSQL through DATABASE_URL
"""

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

def env_bool(name, default=False):
    return os.environ.get(
        name,
        str(default)
    ).strip().lower() in {"1", "true", "yes", "on"}


# Local = True
# Vercel = set DJANGO_DEBUG=0
DEBUG = env_bool("DJANGO_DEBUG", True)


# ============================================================
# SECRET KEY
# ============================================================

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# Local development fallback.
# Vercel will use DJANGO_SECRET_KEY from Environment Variables.
if not SECRET_KEY:
    SECRET_KEY = "django-local-development-secret-key-change-this"


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1,testserver,.vercel.app"
    ).split(",")
    if host.strip()
]


# ============================================================
# CSRF TRUSTED ORIGINS
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "https://*.vercel.app"
    ).split(",")
    if origin.strip()
]


# ============================================================
# SITE URL
# ============================================================

SITE_URL = os.environ.get(
    "SITE_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "main",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Serves static files in production
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL / WSGI
# ============================================================

ROOT_URLCONF = "portfolio.urls"

WSGI_APPLICATION = "portfolio.wsgi.application"

# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

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

# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:

    import dj_database_url

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }

else:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# STATIC FILE STORAGE
# ============================================================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"

    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True


# ============================================================
# EMAIL
# ============================================================

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get(
    "EMAIL_HOST_USER",
    "ntanithasaravanan@gmail.com"
)

EMAIL_HOST_PASSWORD = os.environ.get(
    "EMAIL_HOST_PASSWORD",
    ""
)


if EMAIL_HOST_PASSWORD:

    EMAIL_BACKEND = (
        "django.core.mail.backends.smtp.EmailBackend"
    )

else:

    EMAIL_BACKEND = (
        "django.core.mail.backends.console.EmailBackend"
    )


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"