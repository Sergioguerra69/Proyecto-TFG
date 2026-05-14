# Gestión de consultas veterinarias
# Aquí controlamos todo el flujo de citas de la clínica

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Consulta
from .forms import ConsultaForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# APIs externas para información veterinaria
try:
    from veterinary_apis import VeterinaryAPIManager
    API_MANAGER = VeterinaryAPIManager()
    API_AVAILABLE = True
except ImportError:
    API_MANAGER = None
    API_AVAILABLE = False

@login_required
def lista_consultas(request):
    # Mostramos todas las consultas ordenadas por fecha (más nuevas primero)
    consultas = Consulta.objects.all().order_by('-fecha')
    
    # Información adicional de APIs veterinarias
    api_data = {
        'nearby_clinics': [],      # Clínicas cercanas
        'emergency_clinics': [],   # Urgencias 24h
        'health_tips': []          # Consejos de salud
    }
    
    if API_AVAILABLE and API_MANAGER:
        try:
            # Obtener ubicación del usuario (simulada Madrid)
            lat, lng = 40.4168, -3.7038
            
            # Obtener datos de APIs
            api_data['nearby_clinics'] = API_MANAGER.get_nearby_clinics(lat, lng)[:2]
            api_data['emergency_clinics'] = API_MANAGER.get_emergency_clinics(lat, lng)[:1]
            api_data['health_tips'] = API_MANAGER.get_pet_health_tips('Perro', 'adulto')[:2]
            
            messages.info(request, 'Datos de APIs veterinarias cargados')
        except Exception as e:
            messages.warning(request, f'Error con APIs: {str(e)}')
    
    return render(request, 'consultas/lista_consultas.html', {
        'consultas': consultas,
        'api_data': api_data,
        'api_available': API_AVAILABLE
    })

# CREAR NUEVA CONSULTA - Cuando un cliente pide cita
@login_required
def crear_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)  # Guardamos pero sin confirmar aún
            consulta.estado = 'Pendiente'  # Siempre empieza como pendiente
            consulta.usuario = request.user  # Asignamos el usuario que solicita
            consulta.save()
            
            # Notificación solo al recepcionista
            try:
                from django.contrib.auth.models import User
                # Notificar a recepcionistas (por rol de perfil)
                recepcionistas = User.objects.filter(perfil__rol='recepcionista')
                
                for recepcionista in recepcionistas:
                    from notificaciones.models import Notificacion
                    Notificacion.objects.create(
                        tipo='consulta',
                        objeto_id=consulta.id,
                        emisor=request.user,
                        receptor=recepcionista,
                        estado='pendiente'
                    )
                
                # Notificación en tiempo real al recepcionista
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'clinica_notificaciones',
                    {
                        'type': 'enviar.notificacion',
                        'message': f'Nueva consulta de {consulta.paciente} pendiente de aprobación'
                    }
                )
            except:
                # Si falla el sistema de notificaciones, la web sigue funcionando
                pass
            
            messages.success(request, '¡Consulta solicitada! El recepcionista la revisará pronto.')
            return redirect('lista_consultas')
    else:
        form = ConsultaForm()
    
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Pedir Nueva Consulta Veterinaria',
        'url_cancelar': '/consultas/'
    })

# CAMBIAR ESTADO - Actualizar cómo va la consulta
@login_required
def actualizar_estado_consulta(request, id):
    # TEMPORAL: Cualquier usuario puede cambiar estados (para pruebas)
    pass

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        consulta = get_object_or_404(Consulta, id=id)
        consulta.estado = nuevo_estado
        consulta.save()

        # Notificamos el cambio del estado
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'clinica_notificaciones',
                {
                    'type': 'enviar.notificacion',
                    'message': f'Consulta de {consulta.paciente}: {nuevo_estado}'
                }
            )
        except:
            pass
        
        messages.success(request, f'Estado actualizado a: {nuevo_estado}')
        
    return redirect('lista_consultas')

# EDITAR CONSULTA - Cambiar datos de una cita
@login_required
def editar_consulta(request, id):
    # TEMPORAL: Cualquier usuario puede editar (para pruebas)
    pass
    
    consulta = get_object_or_404(Consulta, id=id)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Consulta actualizada!')
            return redirect('lista_consultas')
    else:
        form = ConsultaForm(instance=consulta)
    
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Editar Datos de la Consulta',
        'url_cancelar': '/consultas/'
    })

# ELIMINAR CONSULTA - Borrar una cita para siempre
@login_required
def eliminar_consulta(request, id):
    # TEMPORAL: Cualquier usuario puede eliminar (para pruebas)
    pass
    
    consulta = get_object_or_404(Consulta, id=id)
    
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'Consulta eliminada')
        return redirect('lista_consultas')
    
    return render(request, 'confirmar_eliminar.html', {
        'objeto': consulta,
        'titulo': '¿Eliminar esta consulta?',
        'url_cancelar': '/consultas/'
    })

# APIs para buscar clínicas cercanas

@login_required
def api_clinics_cercanas(request):
    """Busca clínicas cerca de la ubicación (para AJAX)"""
    if not API_AVAILABLE:
        return JsonResponse({'success': False, 'error': 'API no disponible'})
    
    try:
        lat = float(request.GET.get('lat', 40.4168))
        lng = float(request.GET.get('lng', -3.7038))
        radius = int(request.GET.get('radius', 10))
        
        clinics = API_MANAGER.get_nearby_clinics(lat, lng, radius)
        
        return JsonResponse({
            'success': True,
            'clinics': clinics,
            'total': len(clinics)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
