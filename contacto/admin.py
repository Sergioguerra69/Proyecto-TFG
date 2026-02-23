# Este archivo sirve para que el tutor vea los mensajes desde el panel /admin
from django.contrib import admin
from .models import Consulta

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    # Esto hace que en el admin se vea una tabla con estas columnas
    list_display = ('nombre', 'email', 'asunto', 'fecha')
    # Añadimos un buscador para encontrar mensajes rápido
    search_fields = ('nombre', 'email', 'asunto')
