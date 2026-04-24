from django.contrib import admin
from .models import Analisis

# Configuración del panel de administración para Análisis
@admin.register(Analisis)
class AnalisisAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del admin
    list_display = ('nombre', 'paciente', 'tipo_animal', 'fecha', 'estado')
    
    # Filtros en la barra lateral
    list_filter = ('estado', 'tipo_animal', 'fecha')
    
    # Campos por los que se puede buscar
    search_fields = ('nombre', 'paciente')
    
    # Orden por defecto (más nuevos primero)
    ordering = ('-fecha',)
