from pathlib import Path
import os
from corsheaders.defaults import default_headers
import dj_database_url

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Security / Debug
# -----------------------------
# نجيب القيم من متغيرات البيئة بدل ما تكون ثابتة في الكود

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret")

# الافتراضي True علشان التطوير، وفي السيرفر حط DJANGO_DEBUG=False
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# لو حابب تغيّر ngrok host من غير ما تعدل الكود، استخدم متغير بيئة
NGROK_HOST = os.environ.get(
    "NGROK_HOST",
    "unlubricant-nonqualitative-colton.ngrok-free.dev",  # القيمة القديمة كافتراضي
)

# ALLOWED_HOSTS من env مع قيمة افتراضية مفيدة للتطوير

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".ngrok-free.dev",
    ".ngrok.io",
    ".onrender.com",
    #"web-production-7dcd.up.railway.app",  # الدومين الكامل تبع خدمتك
]


# -----------------------------
# Applications
# -----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",

    "books",
    "accounts",
    "Home",
    "dashboard",
]

# -----------------------------
# REST Framework
# -----------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# -----------------------------
# Middleware
# -----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    "corsheaders.middleware.CorsMiddleware",  # يجب أن يكون مبكراً
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------
# URLs / WSGI
# -----------------------------
ROOT_URLCONF = "Bookshelf.urls"

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Bookshelf.wsgi.application"

# -----------------------------
# Database
# -----------------------------
"""
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get(
            "DATABASE_URL",
            "postgres://postgres:safwan123@localhost:5432/bookshelf"
        ),
        conn_max_age=600,   # اختياري: لتحسين الأداء على السيرفر
    )
}
"""

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'PNefUvyKTPIrlghYQHxGGrXtNlxLSaaI',
        'HOST': 'postgres.railway.internal',
        'PORT': '5432',
    }
}
"""

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get(
            "DATABASE_URL",
            "postgres://postgres:safwan123@localhost:5432/bookshelf"
        ),
        conn_max_age=600,   
    )
}

# -----------------------------
# Password validation
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------
# i18n / TZ
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Damascus"
USE_I18N = True
USE_TZ = True

# -----------------------------
# Static / Media
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # مهم لريندر

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# -----------------------------
# CORS / CSRF
# -----------------------------
#CORS_ALLOWED_ORIGINS = [
 #   "http://localhost:3000",
#]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.ngrok-free\.dev$",
    r"^https://.*\.ngrok\.io$",
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "ngrok-skip-browser-warning",
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{NGROK_HOST}",
]

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")