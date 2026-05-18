# Modelos: clases que representan las tablas de la base de datos
from django.db import models
from django.contrib.auth.models import User

# Tabla para las urgencias que llegan a la clínica
class Urgencia(models.Model):
    # Opciones de prioridad que aparecen en un desplegable
    PRIORIDAD_CHOICES = [
        ('Pendiente', 'Pendiente de Valoración'),
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
        ('Crítica', 'Crítica'),
    ]
    TIPO_ANIMAL_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Roedor', 'Roedor'),
        ('Reptil', 'Reptil'),
        ('Otro', 'Otro'),
    ]
    # Opciones de estado
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
    ]
    # Usuario que solicita la urgencia
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urgencias')
    # Nombre de la mascota o el dueño (legado)
    paciente = models.CharField(max_length=100)
    # Mascota vinculada (nuevo sistema)
    mascota = models.ForeignKey('mascotas.Mascota', on_delete=models.CASCADE, null=True, blank=True, related_name='urgencias')
    # Tipo de animal
    tipo_animal = models.CharField(max_length=20, choices=TIPO_ANIMAL_CHOICES, default='Perro')
    # Especificar otro tipo de animal (cuando selecciona "Otro")
    tipo_animal_otro = models.CharField(max_length=50, blank=True, verbose_name='Especificar otro animal')
    # Cuándo llegó (se pone solo al crear el registro)
    fecha = models.DateTimeField(auto_now_add=True)
    # Indicador del cliente sobre si considera que tiene prioridad
    solicita_prioridad = models.BooleanField(default=False, verbose_name='¿Considera que requiere atención prioritaria inmediata?')
    # Cómo de grave es (lo asigna el veterinario)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='Pendiente')
    # Qué le pasa exactamente
    descripcion = models.TextField()
    # Datos de contacto del solicitante
    dni = models.CharField(max_length=20, blank=True, verbose_name='DNI')
    telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    correo = models.EmailField(blank=True, verbose_name='Correo electrónico')
    # Para saber en qué estado de atención está
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        # Ayuda a identificar la urgencia en el panel de control
        return f"Urgencia: {self.paciente} ({self.prioridad}) - {self.usuario.username}"
