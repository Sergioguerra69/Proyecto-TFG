# Modelos: clases que representan las tablas de la base de datos
from django.db import models
from django.contrib.auth.models import User

# Tabla para guardar las consultas de los animales
class Consulta(models.Model):
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
    # Usuario que solicita la consulta
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultas')
    # Nombre de la mascota o el paciente
    paciente = models.CharField(max_length=100)
    # Tipo de animal (Perro, Gato, Ave, etc.)
    tipo_animal = models.CharField(max_length=20, choices=TIPO_ANIMAL_CHOICES, default='Perro')
    # Especificar otro tipo de animal (cuando selecciona "Otro")
    tipo_animal_otro = models.CharField(max_length=50, blank=True, verbose_name='Especificar otro animal')
    # Veterinario que atiende la consulta
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas_atendidas')
    # Fecha y hora de la cita
    fecha = models.DateTimeField()
    # Por qué viene a la clínica
    motivo = models.TextField()
    # Qué tiene el animal (se rellena después de la consulta)
    diagnostico = models.TextField(blank=True)
    # En qué estado está la consulta
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    # Fecha de creación
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Ayuda a ver de quién es la consulta en el panel de administrador
        return f"Consulta {self.paciente} - {self.fecha.date()} ({self.usuario.username})"
