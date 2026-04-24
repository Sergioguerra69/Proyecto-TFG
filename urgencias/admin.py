from django.contrib import admin
from .models import Urgencia

# Configuración del panel de administración para Urgencias
@admin.register(Urgencia)
class UrgenciaAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del admin
    list_display = ('paciente', 'tipo_animal', 'prioridad', 'fecha', 'estado')
    
    # Filtros en la barra lateral
    list_filter = ('prioridad', 'tipo_animal', 'estado', 'fecha')
    
    # Campos por los que se puede buscar
    search_fields = ('paciente', 'descripcion')
    
    # Orden por defecto (más recientes primero)
    ordering = ('-fecha',)
