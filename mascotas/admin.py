from django.contrib import admin
from .models import Mascota

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'dueno', 'fecha_registro')
    list_filter = ('especie', 'fecha_registro')
    search_fields = ('nombre', 'microchip', 'dueno__username')
