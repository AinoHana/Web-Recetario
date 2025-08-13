# blog-base/apps/usuarios/context_processors.py

from django.apps import apps

def unread_messages_count(request):
    """
    Agrega el conteo de mensajes no leídos al contexto de todas las plantillas
    para los usuarios autenticados.
    """
    # Si el usuario no está autenticado, no tiene mensajes no leídos.
    if not request.user.is_authenticated:
        return {'unread_messages_count': 0}

    try:
        # Usamos apps.get_model para evitar errores de importación circular
        # y para asegurar que los modelos estén listos.
        Mensaje = apps.get_model('usuarios', 'Mensaje')

        # Contar los mensajes no leídos dirigidos al usuario actual.
        # Directamente usamos request.user, ya que el campo 'destinatario'
        # se relaciona con el modelo User, no con Perfil.
        # También corregimos el nombre del campo a 'is_leido'.
        unread_count = Mensaje.objects.filter(
            destinatario=request.user,
            is_leido=False
        ).count()
        
        return {'unread_messages_count': unread_count}

    except Exception as e:
        # En caso de cualquier error (por ejemplo, si el modelo no existe),
        # devolvemos 0 para evitar que la página falle.
        print(f"Error en unread_messages_count context processor: {e}")
        return {'unread_messages_count': 0}