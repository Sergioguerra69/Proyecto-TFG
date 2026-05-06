from django.contrib import admin
from .models import Consulta

# Configuración del panel de administración para Consultas
@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del admin
    list_display = ('paciente', 'tipo_animal', 'veterinario', 'fecha', 'estado')
    
    # Filtros en la barra lateral
    list_filter = ('estado', 'tipo_animal', 'fecha', 'veterinario')
    
    # Campos por los que se puede buscar
    search_fields = ('paciente', 'motivo')
    
    # Orden por defecto (más recientes primero)
    ordering = ('-fecha',)
