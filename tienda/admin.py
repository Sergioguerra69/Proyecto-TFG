from django.contrib import admin
from .models import Producto

# Configuración del panel de administración para Productos
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del admin
    list_display = ('nombre', 'precio', 'stock')
    
    # Filtros en la barra lateral
    list_filter = ('stock',)
    
    # Campos por los que se puede buscar
    search_fields = ('nombre',)
    
    # Orden por defecto (alfabético)
    ordering = ('nombre',)
