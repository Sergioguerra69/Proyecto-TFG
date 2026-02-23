
from django.db import models
from django.contrib.auth.models import User

# Opciones para el rol
OPCIONES_ROL = [
    ('cliente', 'Cliente'),
    ('veterinario', 'Veterinario'),
    ('admin', 'Administrador'),
]

class Perfil(models.Model):
    # Un perfil está relacionado con un usuario de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campos extra
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(max_length=200, blank=True)
    rol = models.CharField(max_length=20, choices=OPCIONES_ROL, default='cliente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"