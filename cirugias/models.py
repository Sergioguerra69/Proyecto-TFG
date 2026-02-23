# Modelos: clases que representan las tablas de la base de datos
from django.db import models

# Tabla para las operaciones en el quirófano (Solo para el Admin)
class Cirugia(models.Model):
    # Estados posibles de una operación
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
    ]
    # Nombre del animal a operar
    paciente = models.CharField(max_length=100)
    # Nombre de la operación (ej. 'Esterilización')
    tipo_cirugia = models.CharField(max_length=100)
    # Fecha de la intervención
    fecha = models.DateTimeField()
    # En qué punto está la operación
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    # En qué sala se hace
    quirofano = models.CharField(max_length=50)

    def __str__(self):
        return f"Cirugía: {self.tipo_cirugia} - {self.paciente}"
