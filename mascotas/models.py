from django.db import models
from django.contrib.auth.models import User

class Mascota(models.Model):
    ESPECIES_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Exótico', 'Exótico'),
        ('Otro', 'Otro'),
    ]

    dueno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mascotas', verbose_name="Dueño")
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50, choices=ESPECIES_CHOICES, default='Perro')
    raza = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Peso en kg")
    microchip = models.CharField(max_length=50, blank=True, null=True, unique=True)
    foto = models.ImageField(upload_to='mascotas/', blank=True, null=True)
    notas_medicas = models.TextField(blank=True, null=True, help_text="Alergias, condiciones crónicas, etc.")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

    def __str__(self):
        return f"{self.nombre} ({self.especie}) - Dueño: {self.dueno.username}"
