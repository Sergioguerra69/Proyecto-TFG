# Este archivo sirve para que el administrador vea los mensajes de contacto desde el panel /admin
from django.contrib import admin
from .models import FormularioContacto, RespuestaContacto

@admin.register(FormularioContacto)
class FormularioContactoAdmin(admin.ModelAdmin):
    # Mostrar las columnas importantes en el admin
    list_display = ('nombre', 'dni', 'email', 'asunto', 'estado', 'fecha_creacion', 'respondido_por')
    # Añadir buscador para encontrar mensajes rápido
    search_fields = ('nombre', 'email', 'asunto', 'dni')
    # Filtros para organizar mejor
    list_filter = ('estado', 'fecha_creacion')
    # Orden por defecto (más recientes primero)
    ordering = ['-fecha_creacion']
    # Solo lectura para algunos campos
    readonly_fields = ('fecha_creacion', 'fecha_respuesta')

@admin.register(RespuestaContacto)
class RespuestaContactoAdmin(admin.ModelAdmin):
    # Mostrar información de respuestas
    list_display = ('formulario', 'autor', 'fecha_creacion')
    # Buscador
    search_fields = ('contenido', 'autor__username')
    # Ordenar por fecha
    ordering = ['-fecha_creacion']
    # Solo lectura
    readonly_fields = ('fecha_creacion',)
