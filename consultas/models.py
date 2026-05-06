# Modelos para gestionar las consultas de la clínica
from django.db import models
from django.contrib.auth.models import User

# Modelo principal para las consultas veterinarias
class Consulta(models.Model):
    # Estados posibles de una consulta
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),        # Esperando aprobación
        ('Aceptada', 'Aceptada'),          # Aprobada por recepción
        ('En Proceso', 'En Proceso'),      # El veterinario la está atendiendo
        ('Completado', 'Completado'),      # Consulta terminada
        ('Rechazada', 'Rechazada'),        # No se pudo atender
    ]
    
    # Tipos de animales que atendemos
    TIPO_ANIMAL_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Roedor', 'Roedor'),
        ('Reptil', 'Reptil'),
        ('Otro', 'Otro'),                  # Animales no listados
    ]
    
    # Dueño de la mascota
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultas')
    
    # Nombre de la mascota
    paciente = models.CharField(max_length=100)
    
    # Tipo de animal (perro, gato, etc.)
    tipo_animal = models.CharField(max_length=20, choices=TIPO_ANIMAL_CHOICES, default='Perro')
    
    # Si es 'Otro', especificar aquí
    tipo_animal_otro = models.CharField(max_length=50, blank=True, verbose_name='Especificar otro animal')
    
    # Veterinario asignado (puede estar vacío)
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas_atendidas')
    
    # Fecha y hora de la cita
    fecha = models.DateTimeField()
    
    # Motivo de la consulta
    motivo = models.TextField()
    
    # Diagnóstico del veterinario
    diagnostico = models.TextField(blank=True)
    
    # Estado actual de la consulta
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    
    # Fecha de creación (automática)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Muestra la consulta en el admin
        # Ejemplo: "Consulta Firulais - 25/12/2024 (juan)"
        return f"Consulta {self.paciente} - {self.fecha.date()} ({self.usuario.username})"
