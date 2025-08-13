from django.contrib import admin
from .models import Receta, Ingrediente, Paso, Comentario, Categoria

# Registramos otros modelos sin clases de administración personalizadas
admin.site.register(Categoria)
admin.site.register(Comentario)

# Para mostrar ingredientes y pasos directamente en el admin de Receta
class IngredienteInline(admin.TabularInline):
    model = Ingrediente
    extra = 1  # Número de campos extra para añadir

class PasoInline(admin.TabularInline):
    model = Paso
    extra = 1

# Usamos el decorador para registrar el modelo Receta con la clase RecetaAdmin.
@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    inlines = [IngredienteInline, PasoInline]
    list_display = ('titulo', 'autor', 'fecha_publicacion', 'categoria', 'is_featured')
    list_editable = ('is_featured',)
    search_fields = ('titulo', 'descripcion', 'autor__username', 'categoria__nombre')
    list_filter = ('autor', 'fecha_publicacion', 'categoria', 'is_featured')