from django.urls import path
from . import views
from apps.usuarios.views import CustomLoginView, CustomLogoutView
from django.contrib import admin

app_name = 'usuarios'

urlpatterns = [
    # URLs de autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # URLs de perfil
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('perfil/editar/', views.perfil_editar, name='editar_perfil'),
    path('perfil/favoritos/', views.perfil_favoritos, name='favoritos_perfil'),
    path('perfil/mis_comentarios/', views.perfil_mis_comentarios, name='mis_comentarios'),

    # URLs de Mensajes Privados
    path('mensajes/', views.inbox, name='inbox'),
    path('mensajes/enviados/', views.sent_messages, name='sent_messages'),
    path('mensajes/compose/', views.compose_message, name='compose_message'),
    path('mensajes/<str:username>/', views.private_message, name='private_message'),
    path('mensajes/eliminar/<int:message_id>/', views.delete_message, name='delete_message'),

    # URLs para favoritos
    path('toggle_favorito/<int:receta_pk>/', views.toggle_favorito, name='toggle_favorito'),
    path('add-to-category/<int:receta_pk>/', views.add_to_category, name='add_to_category'),
]