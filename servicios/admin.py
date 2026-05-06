from django.contrib import admin
from .models import Servicio

# Configuración del panel de administración para Servicios
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del admin
    list_display = ('nombre',)
    
    # Campos por los que se puede buscar
    search_fields = ('nombre', 'descripcion')
    
    # Orden por defecto (alfabético)
    ordering = ('nombre',)
