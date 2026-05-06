# Vistas: funciones que reciben la peticion del usuario y devuelven la pagina HTML
from django.shortcuts import render
from django.http import JsonResponse
from metricas.models import Metrica
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

# Vista de la página principal (Home)
def home(request):
    # Lógica de métricas súper sencilla (Requisito de DAW)
    # Cada vez que alguien entra, sumamos una visita
    visita, created = Metrica.objects.get_or_create(nombre='Visitas Home', defaults={'valor': 0})
    visita.valor += 1
    visita.save()
    
    # Mandamos el contador al HTML para que se vea que funciona
    return render(request, 'inicio/home.html', {'contador_visitas': visita.valor})

# Endpoint para recibir los clics de JavaScript (Métricas)
@csrf_exempt
def clic_metrica(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tipo = data.get('tipo', 'desconocido')
        
        m, created = Metrica.objects.get_or_create(nombre=f"Clic {tipo}", defaults={'valor': 0})
        m.valor += 1
        m.save()
        
        return JsonResponse({'status': 'ok', 'mensaje': 'Métrica guardada'})
    
    return JsonResponse({'status': 'error'}, status=400)

# Vista de 'Sobre Nosotros'
def nosotros(request):
    return render(request, 'inicio/nosotros.html')

# Vista de 'Nuestro Equipo'
def equipo(request):
    return render(request, 'inicio/equipo.html')