"""
Vistas del módulo de Servicios Veterinarios
Implementa API REST y vistas web para gestión de servicios
Autor: [Tu Nombre] - TFG DAW 2025-2026
"""

from django.shortcuts import render
from django.http import JsonResponse
from .models import Servicio

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import ServicioSerializer

def lista_servicios(request):
    """
    Vista web para mostrar catálogo de servicios
    - Recupera todos los servicios disponibles
    - Renderiza template con contexto completo
    """
    servicios = Servicio.objects.all()
    return render(request, 'servicios/servicios.html', {'servicios': servicios})

@api_view(['GET'])
@permission_classes([AllowAny])
def api_servicios(request):
    """
    Endpoint API REST para listado de servicios
    - Implementa serialización DRF para JSON
    - Permite acceso público para demostración
    - Ready para integraciones móviles futuras
    """
    servicios = Servicio.objects.all()
    # Serialización automática via DRF (Data Transformation Layer)
    serializer = ServicioSerializer(servicios, many=True)
    return Response(serializer.data)
