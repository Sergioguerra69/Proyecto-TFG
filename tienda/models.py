# Modelos: clases que representan las tablas de la base de datos
from django.db import models

# Tabla para los productos de la tienda (Piensos, juguetes, collares...)
# Un 'estudiante' diría: "Esta es la base de datos de los productos que vendemos"
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        # Para que en el admin veamos el nombre del producto directamente
        return self.nombre
