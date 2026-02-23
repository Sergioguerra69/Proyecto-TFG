# Modelos: clases que representan las tablas de la base de datos
from django.db import models

# Tabla para los servicios que ofrece la clínica (Cirugía, Consultas, etc.)
# Aquí guardamos lo que la clínica sabe hacer
class Servicio(models.Model):
    # El nombre del servicio (ej. 'Limpieza Dental')
    nombre = models.CharField(max_length=100)
    # Una pequeña explicación para el cliente
    descripcion = models.TextField()
    # Una foto para que la web no sea solo texto
    imagen = models.ImageField(upload_to='servicios/', null=True, blank=True)

    def __str__(self):
        # Muestra el nombre del servicio en el panel de Admin
        return self.nombre
