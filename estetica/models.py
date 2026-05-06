# Modelos: clases que representan las tablas de la base de datos
from django.db import models

# Tabla para los servicios de peluquería y baño
class ServicioEstetica(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
    ]
    # Quién viene a ponerse guapo
    paciente = models.CharField(max_length=100)
    # Qué le vamos a hacer (Corte de pelo, Baño, Uñas...)
    tipo_servicio = models.CharField(max_length=100)
    # Fecha de la cita
    fecha = models.DateTimeField()
    # Notas por si el perro es agresivo o algo similar
    observaciones = models.TextField(blank=True)
    # Control del progreso del servicio
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    class Meta:
        verbose_name = "Servicio de Estética"
        verbose_name_plural = "Servicios de Estética"

    def __str__(self):
        return f"{self.tipo_servicio} - {self.paciente}"
