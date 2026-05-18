"""
Configuración de VetCT
"""

import os
from pathlib import Path
from decouple import config

# Crear carpeta para la base de datos
os.makedirs(os.path.join(Path(__file__).resolve().parent.parent, 'data'), exist_ok=True)

BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta
SECRET_KEY = config('SECRET_KEY', default='clave-secreta-desarrollo-vetct-2024')

# Modo desarrollo o producción
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Aplicaciones de la clínica
INSTALLED_APPS = [
    # Django básico
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Aplicaciones de VetCT
    'inicio',           # Página principal
    'servicios',        # Servicios veterinarios
    'urgencias',        # Urgencias 24h
    'consultas',        # Consulta general
    'laboratorio',      # Análisis y laboratorio
    'estetica',         # Estética y peluquería
    'cirugias',         # Cirugías
    'vacunacion',       # Vacunación
    'tienda',           # Tienda online
    'contacto',         # Formularios de contacto
    'users',
    'mascotas',         # Gestión de Mascotas
    'notificaciones',   # Sistema de notificaciones
    'metricas',         # Métricas del sistema

    # Librerías para WebSockets y API
    'rest_framework',
    'channels',
]


# Configuración de VetCT
VETCT_INFO = {
    'NOMBRE_EMPRESA': 'VetCT',
    'NOMBRE_COMPLETO': 'VetCT - Centro Veterinario Integral',
    'TELEFONO_PRINCIPAL': '+34 912 345 678',
    'TELEFONO_URGENCIAS': '+34 600 123 456',
    'EMAIL_CONTACTO': 'info@vetct.com',
    'DIRECCION': 'Av. Veterinaria 123, Ciudad Animal',
    'HORARIO_NORMAL': 'Lunes a Viernes: 9:00-20:00',
    'HORARIO_FIN_SEMANA': 'Sábados: 10:00-14:00',
    'REDES_SOCIALES': {
        'facebook': 'https://facebook.com/vetct',
        'instagram': 'https://instagram.com/vetct_veterinaria',
        'twitter': 'https://twitter.com/vetct',
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vetct_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates', 
            BASE_DIR / 'inicio/templates',
            BASE_DIR / 'tienda/templates',
            BASE_DIR / 'contacto/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Context processor personalizado para VetCT
                'vetct_web.context_processors.vetct_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'vetct_web.wsgi.application'
ASGI_APPLICATION = 'vetct_web.asgi.application'

# Base de datos
if config('DB_HOST', default=None):
    # Producción con PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASS'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    # Desarrollo local con SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'data' / 'db.sqlite3',
        }
    }

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Idioma y zona horaria
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True  # Traducciones activadas
USE_TZ = True   # Zona horaria activada

# Archivos estáticos (CSS, JS, imágenes)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Archivos subidos por usuarios
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Redis y WebSockets

# Configuración sin Redis (desarrollo)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "vetct-local-cache",
    }
}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Usar Redis solo en producción
redis_url = config('REDIS_URL', default=None)
if redis_url and 'redis:' in redis_url and config('DEBUG', default=True, cast=bool) == False:
    # Usar Redis en producción (DEBUG=False)
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": redis_url,
        }
    }
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [redis_url],
            },
        },
    }

# Tipo de campo de clave primaria
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  
EMAIL_HOST = 'infoVetct@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'