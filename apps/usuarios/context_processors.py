# blog-base/apps/usuarios/context_processors.py

from django.apps import apps
from apps.recetas_app.models import Receta
import random
from django.db.models import Count

def unread_messages_count(request):
    """
    Agrega el conteo de mensajes no leídos al contexto de todas las plantillas
    para los usuarios autenticados.
    """
    # Si el usuario no está autenticado, no tiene mensajes no leídos.
    if not request.user.is_authenticated:
        return {'unread_messages_count': 0}

    try:
        Mensaje = apps.get_model('usuarios', 'Mensaje')

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

# Receta de la semana

def receta_de_la_semana(request):
    """
    A\u00f1ade la receta de la semana al contexto de todas las plantillas.

    Si no hay una receta marcada como 'de la semana', selecciona una receta
    aleatoria como fallback para que el banner siempre muestre algo.
    """
    receta = None

    try:
        # CORRECCIóN: Se elimina el order_by('?') para evitar la selección aleatoria
        # y asegurar que se muestra la receta elegida por el admin.
        receta = Receta.objects.filter(es_receta_de_la_semana=True).first()
    except Exception as e:
        # Captura cualquier otro error, \u00fatil para depurar
        print(f"Error al obtener la receta de la semana: {e}")
        pass

    # Fallback: si no se encontró ninguna receta de la semana,
    # busca una receta popular o aleatoria.
    if not receta:
        try:
            # Opción 1 (Recomendada): Busca una receta popular
            # Obtener el PK de una receta aleatoria entre las 10 más populares
            populares_ids = Receta.objects.annotate(num_likes=Count('likes')).order_by('-num_likes').values_list('pk', flat=True)[:10]
            if populares_ids:
                random_popular_id = random.choice(list(populares_ids))
                receta = Receta.objects.get(pk=random_popular_id)
        except Exception as e:
            print(f"Fallback 1 (populares) falló: {e}")

        # Opción 2 (si la opción 1 falla): Saca una receta completamente aleatoria
        if not receta:
            try:
                recetas_count = Receta.objects.count()
                if recetas_count > 0:
                    random_index = random.randint(0, recetas_count - 1)
                    receta = Receta.objects.all()[random_index]
            except Exception as e:
                 print(f"Fallback 2 (aleatoria) falló: {e}")

    return {'receta_de_la_semana': receta}