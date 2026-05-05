# Perfiles de usuarios de la clínica

from django.db import models
from django.contrib.auth.models import User

# Roles disponibles en la clínica
OPCIONES_ROL = [
    ('cliente', 'Cliente / Dueño de mascota'),
    ('veterinario', 'Veterinario'),
    ('auxiliar', 'Auxiliar Veterinario'),
    ('recepcionista', 'Recepcionista'),
    ('admin', 'Administrador / Director'),
]

class Perfil(models.Model):
    # Cada perfil pertenece a un usuario de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Datos del usuario 
    telefono = models.CharField(max_length=15, blank=True)  # Teléfono de contacto
    direccion = models.TextField(max_length=200, blank=True)  # Dirección del cliente
    especialidad = models.CharField(max_length=100, blank=True)  # Especialidad del veterinario
    es_veterinario = models.BooleanField(default=False)  # Si es veterinario o no
    rol = models.CharField(max_length=20, choices=OPCIONES_ROL, default='cliente')  # Rol en la clínica
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Fecha de registro (automática)
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
    
    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"