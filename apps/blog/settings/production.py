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
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(DB_PATH, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AinoHana$default',
        'USER': 'AinoHana',
        'PASSWORD': 'ElRecetario1234#',
        'HOST': 'AinoHana.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}

os.environ['DJANGO_PORT'] = '8080'
