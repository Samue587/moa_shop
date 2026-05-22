import os
import logging
from pathlib import Path

# ══════════════════════════════════════════════════════
# RUTAS BASE
# ══════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent.parent

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════
# SEGURIDAD
# ══════════════════════════════════════════════════════
SECRET_KEY = 'WxRBkz9vMM-cyOKJd7ihcWTnYvlJtUeF6et-4pnxG81j2QQAyJmgK8s1Xk7KMnLdVDc'
DEBUG = False
ALLOWED_HOSTS = ['*']

# ══════════════════════════════════════════════════════
# APLICACIONES
# ══════════════════════════════════════════════════════
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'AppMoa',
]

# ══════════════════════════════════════════════════════
# MIDDLEWARE
# ══════════════════════════════════════════════════════
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← añadido
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ══════════════════════════════════════════════════════
# URLS Y WSGI
# ══════════════════════════════════════════════════════
ROOT_URLCONF = 'tienda.urls'
WSGI_APPLICATION = 'tienda.wsgi.application'

# ══════════════════════════════════════════════════════
# TEMPLATES
# ══════════════════════════════════════════════════════
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

# ══════════════════════════════════════════════════════
# BASE DE DATOS — Railway MySQL
# ══════════════════════════════════════════════════════
if os.getenv('MYSQLHOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQLDATABASE'),
            'USER': os.getenv('MYSQLUSER'),
            'PASSWORD': os.getenv('MYSQLPASSWORD'),
            'HOST': os.getenv('MYSQLHOST'),
            'PORT': os.getenv('MYSQLPORT'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'connect_timeout': 30,
                'ssl_disabled': True,
            },
            'CONN_MAX_AGE': 0,
        }
    }
else:
    # Local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'TiendaMoa07',
            'USER': 'root',
            'PASSWORD': 'Level_one19',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }

# ══════════════════════════════════════════════════════
# AUTENTICACIÓN PERSONALIZADA
# ══════════════════════════════════════════════════════
AUTHENTICATION_BACKENDS = [
    'AppMoa.backends.EmailBackend',
]

# ══════════════════════════════════════════════════════
# SESIONES
# ══════════════════════════════════════════════════════
SESSION_ENGINE             = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE         = 86400
SESSION_SAVE_EVERY_REQUEST = True

# ══════════════════════════════════════════════════════
# CSRF
# ══════════════════════════════════════════════════════
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://moashop-production.up.railway.app',  # ← esta línea
]

# ══════════════════════════════════════════════════════
# ARCHIVOS ESTÁTICOS
# ══════════════════════════════════════════════════════
STATIC_URL = '/static/'
STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ← añadido
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # ← añadido

# ══════════════════════════════════════════════════════
# MEDIA — imágenes de productos
# ══════════════════════════════════════════════════════
MEDIA_URL  = '/imagenes/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'imagenes')

# ══════════════════════════════════════════════════════
# INTERNACIONALIZACIÓN
# ══════════════════════════════════════════════════════
LANGUAGE_CODE = 'es-co'
TIME_ZONE     = 'America/Bogota'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = False

DECIMAL_SEPARATOR      = ','
THOUSAND_SEPARATOR     = '.'
NUMBER_GROUPING        = 3
USE_THOUSAND_SEPARATOR = True

# ══════════════════════════════════════════════════════
# PK POR DEFECTO
# ══════════════════════════════════════════════════════
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'