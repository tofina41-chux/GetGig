"""
Django settings for getgig project.

Clean Slate: No Admin, Supabase Storage Ecosystem, Local Branding Integration
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# SECURITY & ENVIRONMENT CONFIGURATION
# ==============================================================================

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-m&d3^8v$51_9c!r0_f#k+u(z)w@q=e7xb2p%o*jla-n6h4s')

DEBUG_ENV = os.environ.get('DJANGO_DEBUG')
if DEBUG_ENV is None:
    DEBUG = True
else:
    DEBUG = DEBUG_ENV == 'True'

# Allow Vercel URLs and local development environments
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,.vercel.app').split(',')


# ==============================================================================
# APPLICATION DEFINITION (Admin-Free Minimal Core)
# ==============================================================================
INSTALLED_APPS = [
    # 'jazzmin',                  <-- REMOVED NATIVELY
    # 'django.contrib.admin',     <-- REMOVED NATIVELY
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # WhiteNoise picks up your local static directory files
    'users',
    'projects',
    'storages',
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Intercepts static asset bundles
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'getgig.urls'

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

WSGI_APPLICATION = 'getgig.wsgi.application'


# ==============================================================================
# DATABASES (Local SQLite fallback / Production Supabase Postgres)
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Check for production individual keys injected by the Vercel integration
if os.environ.get('POSTGRES_HOST'):
    db_user = os.environ.get('POSTGRES_USER')
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_host = os.environ.get('POSTGRES_HOST')
    db_database = os.environ.get('POSTGRES_DATABASE')
    
    # Construct a valid PostgreSQL connection URL manually
    constructed_url = f"postgres://{db_user}:{db_password}@{db_host}/{db_database}"
    
    DATABASES['default'] = dj_database_url.config(
        default=constructed_url,
        conn_max_age=600, 
        ssl_require=True
    )


# ==============================================================================
# STATIC & MEDIA FILES CONFIGURATION (Aligned Local Paths & Supabase Backend)
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Fix: Force Django to search your actual raw static file directory 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'getgig', 'static'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Production vs Local Storage Configuration Switch
if not DEBUG:
    # On Vercel, store media payloads in Supabase Storage Buckets
    STORAGES = {
        "default": {
            "BACKEND": "django_supabase_storage.storage.SupabaseStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }
    # Supabase credentials mapped directly to Vercel production environment slots
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")       # This will hold your service_role admin key
    SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET") # Your storage bucket name
else:
    # Local development uses local disk filesystems
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }


# ==============================================================================
# AUTHENTICATION & CORE POLICIES
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = 'users:dashboard_redirect'
LOGOUT_REDIRECT_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ==============================================================================
# PROGRESSIVE WEB APP (PWA) CONFIGURATION
# ==============================================================================

PWA_APP_NAME = 'GetGig'
PWA_APP_DESCRIPTION = "Social Freelancing Marketplace"
PWA_APP_THEME_COLOR = '#0C6FBD'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'

# Aligned directly to map with your custom loaded branding logos
PWA_APP_ICONS = [
    {
        'src': '/static/images/logo.jpg',
        'sizes': '160x160'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com') # Defaults to Gmail
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '') # Your email address
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '') # Your app password
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)