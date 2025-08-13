# usuarios/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Q, Count, Max, F, OuterRef, Subquery

# Modelo de Perfil de Usuario
class Perfil(models.Model):
    # Campo de relación con el usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # Información básica
    avatar = models.ImageField(upload_to='avatares', null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    acerca_de_mi = models.TextField(max_length=500, blank=True, null=True)

    # Información de ubicación y contacto
    localidad = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    movil = models.CharField(max_length=20, blank=True, null=True)

    # Información personal
    fecha_nacimiento = models.DateField(null=True, blank=True)
    mostrar_cumpleanos = models.BooleanField(default=True)
    mostrar_edad = models.BooleanField(default=True)

    # Campos para redes sociales
    twitter = models.CharField(max_length=100, blank=True, null=True, verbose_name="Enlace de Twitter")
    instagram = models.CharField(max_length=100, blank=True, null=True, verbose_name="Enlace de Instagram")
    linkedin = models.CharField(max_length=100, blank=True, null=True, verbose_name="Enlace de LinkedIn")

    # Configuraciones de privacidad y notificaciones
    configuracion_privacidad = models.CharField(
        max_length=20,
        choices=[
            ('publico', 'Público'),
            ('privado', 'Privado'),
            ('seguidores', 'Seguidores')
        ],
        default='publico',
        verbose_name="Configuración de Privacidad"
    )
    recibir_emails_recetas_nuevas = models.BooleanField(default=True, verbose_name="Recibir emails de recetas nuevas")
    recibir_emails_mensajes_privados = models.BooleanField(default=True, verbose_name="Recibir emails de mensajes privados")
    permitir_mensajes_privados = models.BooleanField(default=True, verbose_name="Permitir mensajes privados")

    def __str__(self):
        return f'{self.user.username} Perfil'

    @property
    def edad(self):
        if self.fecha_nacimiento:
            import datetime
            today = datetime.date.today()
            age = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
            return age
        return None

class CategoriaFavorita(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias_favoritas')
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Categoría de Favorito"
        verbose_name_plural = "Categorías de Favoritos"
        unique_together = ('user', 'nombre')

    def __str__(self):
        return f"{self.nombre} ({self.user.username})"

# Managers para el modelo Mensaje
class MensajeManager(models.Manager):
    def get_user_conversations(self, user):
        """
        Retorna las \u00faltimas conversaciones de un usuario de forma eficiente.
        """
        # Subconsulta para obtener el ID del \u00faltimo mensaje de cada conversaci\u00f3n
        latest_message_id = Mensaje.objects.filter(
            Q(remitente=user, destinatario=OuterRef('pk')) | Q(destinatario=user, remitente=OuterRef('pk'))
        ).order_by('-fecha_envio').values('id')[:1]

        # Subconsulta para contar mensajes no le\u00eddos
        unread_count_subquery = Mensaje.objects.filter(
            remitente=OuterRef('pk'),
            destinatario=user,
            is_leido=False
        ).values('remitente').annotate(count=Count('id')).values('count')

        # Obtener los usuarios con los que se ha conversado y anotar con el \u00faltimo mensaje y conteo de no le\u00eddos
        conversations_users = User.objects.filter(
            Q(mensajes_enviados__destinatario=user) | Q(mensajes_recibidos__remitente=user)
        ).distinct().annotate(
            last_message_id=Subquery(latest_message_id),
            unread_count=Subquery(unread_count_subquery)
        )

        conversations_list = []
        for other_user in conversations_users:
            if other_user.last_message_id:
                last_message = Mensaje.objects.get(id=other_user.last_message_id)
                conversations_list.append({
                    'other_user': other_user,
                    'last_message': last_message,
                    'unread_count': other_user.unread_count or 0,
                })

        # Ordenar por fecha del \u00faltimo mensaje
        return sorted(conversations_list, key=lambda x: x['last_message'].fecha_envio, reverse=True)


# Modelo para Mensajes Privados entre Usuarios
class Mensaje(models.Model):
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    asunto = models.CharField(max_length=255)
    cuerpo = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    is_leido = models.BooleanField(default=False)

    objects = MensajeManager()

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name = "Mensaje Privado de Usuarios"
        verbose_name_plural = "Mensajes Privados de Usuarios"

    def __str__(self):
        return f'De: {self.remitente} - Para: {self.destinatario} - Asunto: {self.asunto}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
    else:
        Perfil.objects.create(user=instance)

# Agrega la función is_admin al final del archivo
def is_admin(user):
    """
    Comprueba si el usuario está autenticado y tiene permisos de staff.
    """
    return user.is_authenticated and user.is_staff