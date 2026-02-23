from django.shortcuts import render

# Create your views here.
# inicio/views.py
from django.shortcuts import render

def home(request):
    """Vista principal de la página de inicio"""
    return render(request, 'inicio/home.html')

def nosotros(request):
    """Vista de la página 'Sobre Nosotros'"""
    return render(request, 'inicio/nosotros.html')
def equipo(request):
    """Página del equipo veterinario"""
    return render(request, 'inicio/equipo.html')