# Modelos: clases que representan las tablas de la base de datos
from django.db import models

# Tabla para los análisis de sangre y otras pruebas
class Analisis(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
    ]
    # Nombre de la prueba (ej. 'Hemograma')
    nombre = models.CharField(max_length=100)
    # De quién es la muestra
    paciente = models.CharField(max_length=100)
    # Cuándo se hizo
    fecha = models.DateField()
    # Archivo con los resultados (si lo tenemos en PDF)
    resultado = models.FileField(upload_to='laboratorio/', null=True, blank=True)
    # Comentarios sobre el análisis
    notas = models.TextField(blank=True)
    # Estado del progreso
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return f"{self.nombre} - {self.paciente}"
