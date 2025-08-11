# settings/production.py

from .base import *
import os

# Desactivar el modo de depuración para producción
DEBUG = False

# El dominio de tu aplicación en PythonAnywhere
ALLOWED_HOSTS = ['AinoHana.pythonanywhere.com']

# Cargar la SECRET_KEY desde una variable de entorno para mayor seguridad
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default-fallback-key')

# Configuración de los archivos estáticos y media
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de la base de datos para producción con SQLite 3
# La base de datos debe estar en una carpeta fuera de la aplicación principal para evitar problemas de permisos
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'database')
os.makedirs(DB_PATH, exist_ok=True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DB_PATH, 'db.sqlite3'),
    }
}

# Seguridad adicional para producción
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000 # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
