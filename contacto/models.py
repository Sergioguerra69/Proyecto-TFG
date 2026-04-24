# Modelos: clases que representan las tablas de la base de datos
# Este archivo sirve para guardar los mensajes que nos mandan los clientes
from django.db import models

class Consulta(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True) # Se guarda solo cuando se envía

    class Meta:
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'

    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.asunto}"
