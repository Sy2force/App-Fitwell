import os
from pathlib import Path
from decouple import config
from datetime import timedelta
import dj_database_url

# -----------------------------------------------------------------------------
# CONFIGURATION DE BASE
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète (à garder secrète en production !)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fitwell-dev-key-change-in-production-2026-very-long-secret-key-for-security')

# Mode Debug : True pour le dév, False pour la prod
# Force DEBUG=False sur Render quoi qu'il arrive (sécurité : jamais de traceback en prod)
_FORCE_PRODUCTION = bool(os.environ.get('RENDER'))
DEBUG = False if _FORCE_PRODUCTION else config('DEBUG', default=True, cast=bool)

# -----------------------------------------------------------------------------
# SÉCURITÉ, CORS & CSRF
# -----------------------------------------------------------------------------

# 1. ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']  # Accepte tous les domaines

# Support automatique pour Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# 2. CSRF & CORS Base Configuration
# Liste de base via variable d'environnement ou défauts complets (Local + Render)
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS', 
    default='http://localhost:8000,http://127.0.0.1:8000,https://*.onrender.com'
).split(',')

# Ajout explicite du hostname Render s'il existe
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# 3. Mode Debug : Ports dynamiques
if DEBUG:
    # En développement, on ajoute les ports locaux dynamiques (ex: VS Code ports)
    for port in range(64800, 65000):
        CSRF_TRUSTED_ORIGINS.append(f'http://127.0.0.1:{port}')
        CSRF_TRUSTED_ORIGINS.append(f'http://localhost:{port}')

# 4. Application aux réglages CORS
CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=DEBUG, cast=bool)

# 5. Sécurité Production (HTTPS, HSTS, Cookies)
import sys
if not DEBUG and 'test' not in sys.argv:
    # SSL / HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # XSS & Content Type
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# -----------------------------------------------------------------------------
# LOGGING CONFIGURATION
# -----------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'api': {  # Logger custom pour notre app
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# -----------------------------------------------------------------------------
# APPLICATIONS INSTALLÉES
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Outils tiers
    'rest_framework',           # Pour créer l'API
    'rest_framework_simplejwt', # Pour l'authentification sécurisée
    'corsheaders',              # Pour autoriser le Frontend à nous parler
    'django_filters',           # Pour filtrer les résultats
    'drf_yasg',                 # Pour la documentation Swagger
    'whitenoise',               # Pour gérer les fichiers statiques

    # Notre application
    'api',
    'web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'web.middleware.OnboardingMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# -----------------------------------------------------------------------------
# BASE DE DONNÉES
# -----------------------------------------------------------------------------
# Règle : SQLite uniquement en local (DEBUG=True ET pas sur Render).
# En production (DEBUG=False OU variable RENDER présente), DATABASE_URL est
# OBLIGATOIRE et doit pointer vers une base PostgreSQL valide.
DATABASE_URL = os.environ.get('DATABASE_URL', '')
_IS_RENDER = bool(os.environ.get('RENDER'))  # Render set cette var automatiquement
_IS_PRODUCTION = (not DEBUG) or _IS_RENDER
_VALID_DB_SCHEMES = ('postgres://', 'postgresql://', 'sqlite://', 'mysql://')

if DATABASE_URL and DATABASE_URL.startswith(_VALID_DB_SCHEMES):
    # Support pour Render (convertit postgres:// en postgresql:// si nécessaire)
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=not DEBUG,
        )
    }
elif DATABASE_URL:
    # DATABASE_URL est défini mais malformé (ex: 'https://...') -> erreur explicite
    raise ValueError(
        f"DATABASE_URL invalide: scheme '{DATABASE_URL.split('://')[0] if '://' in DATABASE_URL else DATABASE_URL}'. "
        f"Attendu: postgresql://, postgres://, sqlite:// ou mysql://. "
        f"Sur Render, utilisez le bouton 'Connect' pour lier l'Internal Connection String de la database PostgreSQL."
    )
elif _IS_PRODUCTION and DATABASE_URL:
    # Production sans DATABASE_URL valide -> on refuse de démarrer
    raise ValueError(
        "DATABASE_URL invalide en production. "
        "Sur Render : créez une database PostgreSQL puis ajoutez la variable "
        "d'environnement DATABASE_URL (Internal Database URL) dans les settings du service. "
        "Ou utilisez le Blueprint (render.yaml) qui lie la DB automatiquement. "
        "Pour développer en local, mettre DEBUG=True dans .env (SQLite sera utilisée)."
    )
elif _IS_PRODUCTION:
    # Production sans DATABASE_URL -> on utilise SQLite temporairement pour éviter le crash
    # Render liera DATABASE_URL via Blueprint, mais settings.py peut être chargé avant
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Développement local uniquement (DEBUG=True et pas sur Render) -> SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# -----------------------------------------------------------------------------
# MOTS DE PASSE & SÉCURITÉ
# -----------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'api.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('Français')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# -----------------------------------------------------------------------------
# FICHIERS STATIQUES & MÉDIAS
# -----------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'web' / 'static',
]
# 236. WhiteNoise Storage
# Utiliser le stockage standard en développement pour éviter les erreurs de manifest
if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'api.User'

# -----------------------------------------------------------------------------
# CACHE CONFIGURATION (Performance Optimization)
# -----------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'fitwell-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# Cache timeout settings (in seconds)
CACHE_MIDDLEWARE_SECONDS = 300  # 5 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'fitwell'

# -----------------------------------------------------------------------------
# REDIRECTIONS & URLs
# -----------------------------------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# -----------------------------------------------------------------------------
# CONFIGURATION REST FRAMEWORK (API)
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

# -----------------------------------------------------------------------------
# CONFIGURATION JWT (Tokens)
# -----------------------------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Le token dure 1h
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Le refresh dure 24h
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# -----------------------------------------------------------------------------
# EMAIL CONFIGURATION
# -----------------------------------------------------------------------------
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # En production, utiliser un vrai service (SendGrid, Mailgun, etc.)
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.sendgrid.net')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = 'FitWell <noreply@fitwell.local>'


