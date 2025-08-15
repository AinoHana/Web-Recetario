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
    list_display = ('titulo', 'autor', 'fecha_publicacion', 'categoria', 'receta_de_la_semana_display')
    list_editable = ('is_featured',)
    search_fields = ('titulo', 'descripcion', 'autor__username', 'categoria__nombre')
    list_filter = ('autor', 'fecha_publicacion', 'categoria', 'is_featured')

# Campo calculado para mejorar la visualización en el admin
    def receta_de_la_semana_display(self, obj):
        return obj.is_featured

    # Añadimos un 'short_description' para que el encabezado de la columna sea más claro
    receta_de_la_semana_display.short_description = 'Receta de la Semana'

    # También permitimos ordenar por este campo
    receta_de_la_semana_display.admin_order_field = 'is_featured'

    # Para que el campo sea editable en la lista, el nombre del campo
    # 'is_featured' debe estar en 'list_editable'.
    list_editable = ('is_featured',)