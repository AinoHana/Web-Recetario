from django.apps import AppConfig

class UsuariosAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usuarios'
    label = 'usuarios'
    verbose_name = 'Gestión de Usuarios'