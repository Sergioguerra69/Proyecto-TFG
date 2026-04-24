from django.contrib import admin
from .models import ServicioEstetica

# Configuración del panel de administración para Servicios de Estética
@admin.register(ServicioEstetica)
class ServicioEsteticaAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del admin
    list_display = ('paciente', 'tipo_servicio', 'fecha', 'estado')
    
    # Filtros en la barra lateral
    list_filter = ('estado', 'fecha', 'tipo_servicio')
    
    # Campos por los que se puede buscar
    search_fields = ('paciente', 'tipo_servicio')
    
    # Orden por defecto (más recientes primero)
    ordering = ('-fecha',)
