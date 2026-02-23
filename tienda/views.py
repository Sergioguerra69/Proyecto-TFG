"""
Vistas del módulo de Tienda Online
Gestiona el catálogo de productos para la veterinaria
Autor: [Tu Nombre] - TFG DAW 2025-2026
"""

from django.shortcuts import render
from .models import Producto

def lista_productos(request):
    """
    Vista principal del catálogo de productos
    - Recupera productos ordenados alfabéticamente
    - Renderiza template con contexto de productos
    - Optimizada para SEO con estructura clara
    """
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'tienda/tienda.html', {'productos': productos})
