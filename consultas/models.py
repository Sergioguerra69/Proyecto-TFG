# Modelos: clases que representan las tablas de la base de datos
from django.db import models

# Tabla para guardar las consultas de los animales
class Consulta(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
    ]
    # Nombre de la mascota o el paciente
    paciente = models.CharField(max_length=100)
    # Nombre del veterinario que le atiende
    veterinario = models.CharField(max_length=100)
    # Fecha y hora de la cita
    fecha = models.DateTimeField()
    # Por qué viene a la clínica
    motivo = models.TextField()
    # Qué tiene el animal (se rellena después de la consulta)
    diagnostico = models.TextField(blank=True)
    # En qué estado está la consulta
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        # Ayuda a ver de quién es la consulta en el panel de administrador
        return f"Consulta {self.paciente} - {self.fecha.date()}"
