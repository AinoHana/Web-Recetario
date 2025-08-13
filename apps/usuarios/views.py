# apps/usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserUpdateForm, PerfilUpdateForm, SeguridadPerfilForm, CategoriaFavoritaForm, MensajeForm
from .models import Perfil, CategoriaFavorita, Mensaje
from apps.recetas_app.models import Receta, Comentario, RecetaFavorita

def registro(request):
    """
    Vista para el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy('recetas_app:home'))
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registration/registro.html', {'form': form})

class CustomLoginView(LoginView):
    """
    Vista personalizada para el login.
    """
    template_name = 'usuarios/registration/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    """
    Vista personalizada para el logout.
    """
    next_page = reverse_lazy('recetas_app:home')

@login_required
def perfil_editar(request):
    """
    Vista para editar el perfil del usuario.
    """
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            perfil_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
            password_form = PasswordChangeForm(user=request.user)

            if user_form.is_valid() and perfil_form.is_valid():
                user_form.save()
                perfil_form.save()
                messages.success(request, '¡Tu perfil se ha actualizado correctamente!')
                return redirect('usuarios:ver_perfil')
            else:
                messages.error(request, 'Hubo un error al actualizar el perfil. Por favor, revisa los campos a continuación.')
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error en el campo de usuario "{field}": {error}')
                for field, errors in perfil_form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error en el campo de perfil "{field}": {error}')
        elif form_type == 'password':
            user_form = UserUpdateForm(instance=request.user)
            perfil_form = PerfilUpdateForm(instance=request.user.perfil)
            password_form = PasswordChangeForm(user=request.user, data=request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, '¡Tu contraseña se ha cambiado con éxito!')
                return redirect('usuarios:editar_perfil')
            else:
                messages.error(request, 'Por favor, corrige los errores del formulario de contraseña.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        perfil_form = PerfilUpdateForm(instance=request.user.perfil)
        password_form = PasswordChangeForm(user=request.user)

    context = {
        'user_form': user_form,
        'perfil_form': perfil_form,
        'password_form': password_form,
        'user': request.user
    }
    return render(request, 'usuarios/perfil_editar.html', context)

@login_required
def perfil_favoritos(request):
    """
    Vista para gestionar las recetas y categorías favoritas.
    """
    recetas_favoritas = RecetaFavorita.objects.filter(usuario=request.user).order_by('-fecha_agregado')
    categorias_favoritas = CategoriaFavorita.objects.filter(user=request.user).order_by('nombre')

    if request.method == 'POST':
        categoria_form = CategoriaFavoritaForm(request.POST)
        if categoria_form.is_valid():
            nueva_categoria = categoria_form.save(commit=False)
            nueva_categoria.user = request.user
            nueva_categoria.save()
            return redirect('usuarios:favoritos_perfil')
    else:
        categoria_form = CategoriaFavoritaForm()

    return render(request, 'usuarios/perfil_favoritos.html', {
        'recetas_favoritas': recetas_favoritas,
        'categorias_favoritas': categorias_favoritas,
        'categoria_form': categoria_form,
        'user': request.user
    })

@login_required
def perfil_mis_comentarios(request):
    """
    Vista para ver los comentarios del usuario.
    """
    comentarios_principales = Comentario.objects.filter(
        autor=request.user,
        respuesta_a__isnull=True
    ).order_by('-fecha_creacion')

    return render(request, 'usuarios/perfil_mis_comentarios.html', {
        'comentarios_principales': comentarios_principales,
        'user': request.user
    })

@login_required
def ver_perfil(request):
    """
    Vista para ver el perfil público del usuario.
    """
    perfil = request.user.perfil
    recetas_favoritas = RecetaFavorita.objects.filter(usuario=request.user).order_by('-fecha_agregado')
    ultimos_comentarios = Comentario.objects.filter(autor=request.user).order_by('-fecha_creacion')[:5]

    favoritos_por_categoria = {}
    for fav in recetas_favoritas:
        categoria_nombre = fav.categoria.nombre if fav.categoria else "Sin Categoría"
        if categoria_nombre not in favoritos_por_categoria:
            favoritos_por_categoria[categoria_nombre] = []
        favoritos_por_categoria[categoria_nombre].append(fav)

    context = {
        'perfil': perfil,
        'recetas_favoritas': recetas_favoritas,
        'ultimos_comentarios': ultimos_comentarios,
        'favoritos_por_categoria': favoritos_por_categoria,
        'user': request.user,
    }
    return render(request, 'usuarios/ver_perfil.html', context)

# VISTAS DE MENSAJES PRIVADOS (ACTUALIZADAS)
@login_required
def perfil_usuario(request, username):
    """
    Muestra el perfil de un usuario.
    """
    perfil = get_object_or_404(Perfil, user__username=username)
    context = {
        'perfil': perfil,
        'page_title': 'Perfil de ' + username
    }
    return render(request, 'usuarios/perfil.html', context)

@login_required
def inbox(request):
    """
    Muestra la bandeja de entrada del usuario con la última conversación por remitente.
    """
    mensajes_recibidos = Mensaje.objects.filter(destinatario=request.user).order_by('-fecha_envio')
    conversaciones = {}
    for mensaje in mensajes_recibidos:
        if mensaje.remitente not in conversaciones:
            conversaciones[mensaje.remitente] = mensaje
    context = {
        'page_title': 'Bandeja de Entrada',
        'conversations': conversaciones,
        'active_tab': 'inbox'
    }
    return render(request, 'usuarios/inbox.html', context)

@login_required
def sent_messages(request):
    """
    Muestra los mensajes enviados por el usuario.
    """
    mensajes_enviados = Mensaje.objects.filter(remitente=request.user).order_by('-fecha_envio')
    conversaciones = {}
    for mensaje in mensajes_enviados:
        if mensaje.destinatario not in conversaciones:
            conversaciones[mensaje.destinatario] = mensaje
    context = {
        'page_title': 'Mensajes Enviados',
        'conversations': conversaciones,
        'active_tab': 'sent'
    }
    return render(request, 'usuarios/sent_messages.html', context)

@login_required
def compose_message(request, recipient_username=None):
    """
    Maneja la lógica para crear un nuevo mensaje.
    Si se especifica un destinatario, se pre-completa el campo.
    """
    form = MensajeForm(request.POST or None)
    if recipient_username:
        try:
            recipient_user = User.objects.get(username=recipient_username)
            form.fields['destinatario'].initial = recipient_user.pk
        except User.DoesNotExist:
            messages.error(request, 'El usuario destinatario no existe.')
            return redirect('usuarios:compose_message')

    if request.method == 'POST':
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.save()
            messages.success(request, '¡Mensaje enviado exitosamente!')
            return redirect('usuarios:inbox')

    context = {
        'form': form,
        'page_title': 'Nuevo Mensaje',
        'active_tab': 'compose'
    }
    return render(request, 'usuarios/compose_message.html', context)

@login_required
def private_message(request, username):
    """
    Muestra una conversaci\u00f3n privada con otro usuario y permite responder.
    """
    other_user = get_object_or_404(User, username=username)
    mensajes_privados = Mensaje.objects.filter(
        Q(remitente=request.user, destinatario=other_user) |
        Q(remitente=other_user, destinatario=request.user)
    ).order_by('fecha_envio')

    # Marca como le\u00eddos los mensajes recibidos del otro usuario
    received_messages = mensajes_privados.filter(destinatario=request.user, is_leido=False)
    received_messages.update(is_leido=True)

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.remitente = request.user
            message.destinatario = other_user
            message.save()
            return redirect('usuarios:private_message', username=username)
    else:
        form = MensajeForm()

    context = {
        'page_title': f'Conversaci\u00f3n con {username}',
        'other_user': other_user,
        'mensajes_privados': mensajes_privados,
        'form': form,
    }
    return render(request, 'usuarios/private_message.html', context)

@require_POST
@login_required
def toggle_favorito(request, receta_pk):
    """
    Añade o quita una receta de favoritos y devuelve una respuesta JSON.
    """
    receta = get_object_or_404(Receta, pk=receta_pk)
    favorito_existente = RecetaFavorita.objects.filter(usuario=request.user, receta=receta)
    is_favorited = False
    if favorito_existente.exists():
        favorito_existente.delete()
        is_favorited = False
    else:
        RecetaFavorita.objects.create(usuario=request.user, receta=receta)
        is_favorited = True
    return JsonResponse({'is_favorited': is_favorited})

@login_required
def add_to_category(request, receta_pk):
    """
    Añade una receta favorita a una categoría específica.
    """
    receta = get_object_or_404(Receta, pk=receta_pk)
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        if categoria_id:
            categoria = get_object_or_404(CategoriaFavorita, pk=categoria_id, user=request.user)
            receta_favorita, created = RecetaFavorita.objects.get_or_create(usuario=request.user, receta=receta)
            receta_favorita.categoria = categoria
            receta_favorita.save()
    return redirect('recetas_app:detalle_receta', pk=receta_pk)