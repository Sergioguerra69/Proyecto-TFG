# Modelos: clases que representan las tablas de la base de datos

from django.db import models
from django.contrib.auth.models import User

# Roles para una clínica veterinaria
OPCIONES_ROL = [
    ('cliente', 'Cliente / Dueño de mascota'),
    ('veterinario', 'Veterinario'),
    ('auxiliar', 'Auxiliar Veterinario'),
    ('recepcionista', 'Recepcionista'),
    ('admin', 'Administrador / Director'),
]

class Perfil(models.Model):
    # Un perfil está relacionado con un usuario de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campos 
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(max_length=200, blank=True)
    especialidad = models.CharField(max_length=100, blank=True)
    es_veterinario = models.BooleanField(default=False)
    rol = models.CharField(max_length=20, choices=OPCIONES_ROL, default='cliente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
    
    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"