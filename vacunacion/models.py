# Modelos: clases que representan las tablas de la base de datos
from django.db import models
from mascotas.models import Mascota

class Vacuna(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='vacunas')
    nombre = models.CharField(max_length=100, help_text="Ej: Rabia, Parvovirus, etc.")
    fecha_aplicacion = models.DateField()
    proxima_dosis = models.DateField(null=True, blank=True)
    lote = models.CharField(max_length=50, blank=True)
    veterinario_aplicador = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = "Vacuna"
        verbose_name_plural = "Vacunas"
        ordering = ['-fecha_aplicacion']

    def __str__(self):
        return f"{self.nombre} - {self.mascota.nombre} ({self.fecha_aplicacion})"
