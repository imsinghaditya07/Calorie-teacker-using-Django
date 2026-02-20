from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Core Security ─────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production-please-use-env-var')
DEBUG = config('DEBUG', default=False, cast=bool)

# Detect Vercel environment
VERCEL = os.environ.get('VERCEL', '') == '1'

# ── Allowed Hosts ─────────────────────────────────────────────────────────────
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
# Strip whitespace from each host
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h.strip()]

if VERCEL:
    ALLOWED_HOSTS += ['.vercel.app', '.now.sh']
    # Also allow the auto-injected VERCEL_URL
    vercel_url = os.environ.get('VERCEL_URL', '')
    if vercel_url and vercel_url not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(vercel_url)

# ── CSRF Trusted Origins ───────────────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost:8000,http://127.0.0.1:8000'
).split(',')
CSRF_TRUSTED_ORIGINS = [o.strip() for o in CSRF_TRUSTED_ORIGINS if o.strip()]

if VERCEL:
    CSRF_TRUSTED_ORIGINS.append('https://*.vercel.app')
    vercel_url = os.environ.get('VERCEL_URL', '')
    if vercel_url:
        CSRF_TRUSTED_ORIGINS.append(f'https://{vercel_url}')

# ── Installed Apps ────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'calories',
]

# ── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files efficiently
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'calorie_counter.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'calorie_counter.wsgi.application'

# ── Database ──────────────────────────────────────────────────────────────────
# NOTE: SQLite does NOT work on Vercel (read-only filesystem).
# Set DATABASE_URL in Vercel env vars using a free Neon PostgreSQL database.
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=VERCEL,  # Require SSL on Vercel/production
        )
    }
elif VERCEL:
    raise RuntimeError(
        'DATABASE_URL is required on Vercel. '
        'Create a free Neon PostgreSQL database at https://neon.tech and add DATABASE_URL to your Vercel env vars.'
    )
else:
    # Local development — SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ── Auth ──────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ── Localisation ──────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ── Static Files ──────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise: serve compressed static files with long-lived cache headers
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Security (always-on basics) ───────────────────────────────────────────────
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# ── Security (production only) ────────────────────────────────────────────────
if not DEBUG:
    # Vercel handles SSL at the edge — don't redirect to HTTPS inside Django
    # (it causes infinite redirect loops behind Vercel's proxy).
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    # Tell Django to trust Vercel's forwarded HTTPS header
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
