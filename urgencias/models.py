# Modelos: clases que representan las tablas de la base de datos
from django.db import models

# Tabla para las urgencias que llegan a la clínica
class Urgencia(models.Model):
    # Opciones de prioridad que aparecen en un desplegable
    PRIORIDAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
        ('Crítica', 'Crítica'),
    ]
    # Opciones de estado
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
    ]
    # Nombre de la mascota o el dueño
    paciente = models.CharField(max_length=100)
    # Cuándo llegó (se pone solo al crear el registro)
    fecha = models.DateTimeField(auto_now_add=True)
    # Cómo de grave es
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES)
    # Qué le pasa exactamente
    descripcion = models.TextField()
    # Para saber en qué estado de atención está
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        # Ayuda a identificar la urgencia en el panel de control
        return f"Urgencia: {self.paciente} ({self.prioridad})"
