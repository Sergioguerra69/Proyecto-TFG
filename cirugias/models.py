# Modelos: clases que representan las tablas de la base de datos
from django.db import models
from django.contrib.auth.models import User

# Tabla para las operaciones en el quirófano (Solo para el Admin)
class Cirugia(models.Model):
    # Estados posibles de una operación
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
    ]
    TIPO_ANIMAL_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Roedor', 'Roedor'),
        ('Reptil', 'Reptil'),
        ('Otro', 'Otro'),
    ]
    # Usuario que solicita la cirugía
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cirugias')
    # Nombre del animal a operar
    paciente = models.CharField(max_length=100)
    # Tipo de animal
    tipo_animal = models.CharField(max_length=20, choices=TIPO_ANIMAL_CHOICES, default='Perro')
    # Especificar otro tipo de animal (cuando selecciona "Otro")
    tipo_animal_otro = models.CharField(max_length=50, blank=True, verbose_name='Especificar otro animal')
    # Nombre de la operación (ej. 'Esterilización')
    tipo_cirugia = models.CharField(max_length=100)
    # Fecha de la intervención
    fecha = models.DateTimeField()
    # Veterinario responsable de la cirugía
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cirugias_realizadas')
    # En qué punto está la operación
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    # En qué sala se hace
    quirofano = models.CharField(max_length=50)
    # Fecha de creación
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cirugía"
        verbose_name_plural = "Cirugías"

    def __str__(self):
        return f"{self.tipo_cirugia} - {self.paciente} ({self.usuario.username})"
