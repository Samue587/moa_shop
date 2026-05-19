from pathlib import Path
import os

# ══════════════════════════════════════════════════════
# RUTAS BASE
# ══════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent.parent

# ══════════════════════════════════════════════════════
# SEGURIDAD
# ══════════════════════════════════════════════════════
SECRET_KEY = 'django-insecure-cambia-esto-por-una-clave-segura-en-produccion'
DEBUG = True
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
    'django.contrib.humanize',  # para |intcomma en templates
    'AppMoa',                   # app principal
]

# ══════════════════════════════════════════════════════
# MIDDLEWARE
# ══════════════════════════════════════════════════════
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
# Busca en TiendaMoa07/templates/
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
# BASE DE DATOS — MySQL
# ══════════════════════════════════════════════════════
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'TiendaMoa07',       # nombre de tu base de datos en MySQL
        'USER':     'root',              # tu usuario MySQL
        'PASSWORD': 'Level_one19',  # tu contraseña MySQL
        'HOST':     '127.0.0.1',
        'PORT':     '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# ══════════════════════════════════════════════════════
# AUTENTICACIÓN PERSONALIZADA
# Usamos nuestro propio backend con email + contrasena
# ══════════════════════════════════════════════════════
AUTHENTICATION_BACKENDS = [
    'AppMoa.backends.EmailBackend',
]

# ══════════════════════════════════════════════════════
# SESIONES
# ══════════════════════════════════════════════════════
SESSION_ENGINE             = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE         = 86400          # 24 horas
SESSION_SAVE_EVERY_REQUEST = True

# ══════════════════════════════════════════════════════
# CSRF
# ══════════════════════════════════════════════════════
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# ══════════════════════════════════════════════════════
# ARCHIVOS ESTÁTICOS
# ══════════════════════════════════════════════════════
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]   # opcional para archivos estáticos globales

# ══════════════════════════════════════════════════════
# MEDIA — imágenes de productos
# Acceso:  /imagenes/<nombre_archivo>
# Disco:   TiendaMoa07/imagenes/<nombre_archivo>
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
USE_TZ        = False   # hora local Bogotá, no UTC

# Formato peso colombiano
DECIMAL_SEPARATOR      = ','
THOUSAND_SEPARATOR     = '.'
NUMBER_GROUPING        = 3
USE_THOUSAND_SEPARATOR = True

# ══════════════════════════════════════════════════════
# PK POR DEFECTO
# ══════════════════════════════════════════════════════
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'