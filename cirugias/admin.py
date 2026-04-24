from django.contrib import admin
from .models import Cirugia

# Configuración del panel de administración para Cirugías
@admin.register(Cirugia)
class CirugiaAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del admin
    list_display = ('paciente', 'tipo_animal', 'tipo_cirugia', 'veterinario', 'fecha', 'estado', 'quirofano')
    
    # Filtros en la barra lateral
    list_filter = ('estado', 'tipo_animal', 'fecha', 'quirofano', 'veterinario')
    
    # Campos por los que se puede buscar
    search_fields = ('paciente', 'tipo_cirugia')
    
    # Orden por defecto (más recientes primero)
    ordering = ('-fecha',)
