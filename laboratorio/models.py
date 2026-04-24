# Modelos: clases que representan las tablas de la base de datos
from django.db import models
from django.contrib.auth.models import User

# Tabla para los análisis de sangre y otras pruebas
class Analisis(models.Model):
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
    # Usuario que solicita el análisis
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analisis')
    # Nombre de la prueba (ej. 'Hemograma')
    nombre = models.CharField(max_length=100)
    # De quién es la muestra
    paciente = models.CharField(max_length=100)
    # Tipo de animal
    tipo_animal = models.CharField(max_length=20, choices=TIPO_ANIMAL_CHOICES, default='Perro')
    # Especificar otro tipo de animal (cuando selecciona "Otro")
    tipo_animal_otro = models.CharField(max_length=50, blank=True, verbose_name='Especificar otro animal')
    # Cuándo se hizo
    fecha = models.DateField()
    # Archivo con los resultados (si lo tenemos en PDF)
    resultado = models.FileField(upload_to='laboratorio/', null=True, blank=True)
    # Comentarios sobre el análisis
    notas = models.TextField(blank=True)
    # Estado del progreso
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    # Fecha de creación
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Análisis"
        verbose_name_plural = "Análisis"

    def __str__(self):
        return f"{self.nombre} - {self.paciente} ({self.usuario.username})"
