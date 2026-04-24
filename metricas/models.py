# Modelos: clases que representan las tablas de la base de datos
from django.db import models

# Tabla para guardar métricas que pide el profesor de DAW
class Metrica(models.Model):
    # Nombre de la métrica (ej: "Visitas de la Home")
    nombre = models.CharField(max_length=100)
    # El valor del contador
    valor = models.FloatField()
    # Cuándo se registró por última vez
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Para que en el admin de Django se vea bonito
        return f"{self.nombre}: {self.valor}"
