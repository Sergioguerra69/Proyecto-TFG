from rest_framework import serializers
from .models import Servicio

# Serializador para convertir los modelos a JSON (Estándar de la industria)
# Muy fácil de explicar: mapea los campos de la base de datos automáticamente
class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'imagen']
