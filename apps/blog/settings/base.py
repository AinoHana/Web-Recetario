from pathlib import Path
import os
from django.urls import reverse_lazy

# BASE_DIR ahora apunta a la carpeta 'blog-base' (raíz del repositorio)
# __file__ es base.py (en settings/)
# .parent es settings/
# .parent.parent es blog/
# .parent.parent.parent es apps/
# .parent.parent.parent.parent es blog-base/
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

SECRET_KEY = 'django-insecure-&vznf9d1ub9b7!@ecs)&s+em1z%hwn9+nkqqvsge$+j%q$xf@k'

DEBUG = True

ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = reverse_lazy('recetas_app:home')
LOGOUT_REDIRECT_URL = reverse_lazy('recetas_app:home')
LOGIN_URL = reverse_lazy('usuarios:login')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.recetas_app.apps.RecetasAppConfig',
    'apps.usuarios.apps.UsuariosAppConfig',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'apps.blog.urls' 
WSGI_APPLICATION = 'apps.blog.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates' / 'recetas_app',
            BASE_DIR / 'templates' / 'usuarios',
        ], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'usuarios.context_processors.unread_messages_count',
            ],
        },
    },
]

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'