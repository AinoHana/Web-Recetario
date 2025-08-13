# usuarios/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Perfil, CategoriaFavorita, Mensaje

# Formulario de Registro Personalizado
class RegistroForm(UserCreationForm):
    email = forms.EmailField(label='Correo', required=True)
    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellido', required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

# ==========================================================
# CAMBIO CLAVE AQUÍ: Se eliminó 'username' y 'last_name' de la lista de campos.
# El formulario ahora solo valida 'first_name' y 'email'.
# ==========================================================
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Nombre')

    class Meta:
        model = User
        fields = ['first_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'placeholder': 'tuemail@ejemplo.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})

# Formulario para actualizar los campos de nuestro modelo Perfil
class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'avatar',
            'nickname',
            'fecha_nacimiento',
            'localidad',
            'acerca_de_mi',
            'movil',
            'mostrar_cumpleanos',
            'twitter',
            'instagram',
            'linkedin',
        ]
        labels = {
            'avatar': 'Cambiar Avatar',
            'nickname': 'Nickname',
            'fecha_nacimiento': 'Cumpleaños',
            'localidad': 'Ubicación',
            'acerca_de_mi': 'Acerca de mí',
            'movil': 'Móvil',
            'mostrar_cumpleanos': 'Mostrar mi cumpleaños en mi perfil público',
            'twitter': 'Twitter',
            'instagram': 'Instagram',
            'linkedin': 'LinkedIn',
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'acerca_de_mi': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Cuéntanos algo sobre ti...'}),
            'localidad': forms.TextInput(attrs={'placeholder': 'Ej. Ciudad de México'}),
            'movil': forms.TextInput(attrs={'placeholder': 'Ej. +52123456789'}),
            'nickname': forms.TextInput(attrs={'placeholder': 'Ej. ChefPilar'}),
            'twitter': forms.URLInput(attrs={'placeholder': 'URL de tu perfil de Twitter'}),
            'instagram': forms.URLInput(attrs={'placeholder': 'URL de tu perfil de Instagram'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'URL de tu perfil de LinkedIn'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['avatar', 'mostrar_cumpleanos']:
                field.widget.attrs.update({'class': 'form-input'})

# Formulario para el cambio de contraseña
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña Actual', 'class': 'form-control'}),
        label="Contraseña Actual"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva Contraseña', 'class': 'form-control'}),
        label="Nueva Contraseña"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña', 'class': 'form-control'}),
        label="Confirmar Contraseña"
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

# Formulario para las preferencias de seguridad y notificaciones
class SeguridadPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'recibir_emails_recetas_nuevas',
            'recibir_emails_mensajes_privados',
            'permitir_mensajes_privados',
            'mostrar_cumpleanos',
            'mostrar_edad',
        ]

#Formulario para crear una categoría de favoritos
class CategoriaFavoritaForm(forms.ModelForm):
    class Meta:
        model = CategoriaFavorita
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la Categoría',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Postres, Cenas Rápidas'}),
        }

# Formulario para enviar mensajes privados (Consolidado)
class MensajeForm(forms.ModelForm):
    destinatario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Destinatario",
        empty_label="Selecciona un usuario",
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Mensaje
        fields = ['destinatario', 'asunto', 'cuerpo']
        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Asunto (Opcional)'}),
            'cuerpo': forms.Textarea(attrs={'class': 'form-input', 'rows': 5, 'placeholder': 'Escribe tu mensaje...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Excluye al usuario actual de la lista de destinatarios
            self.fields['destinatario'].queryset = User.objects.all().exclude(pk=user.pk)