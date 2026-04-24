# Vistas del módulo de Consultas
# Aquí gestionamos las consultas médicas con integración de APIs

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

# Importar sistema de APIs veterinarias
try:
    from veterinary_apis import VeterinaryAPIManager
    API_MANAGER = VeterinaryAPIManager()
    API_AVAILABLE = True
except ImportError:
    API_MANAGER = None
    API_AVAILABLE = False

@login_required  # El usuario debe estar logueado
def lista_consultas(request):
    # Mostramos todas las consultas ordenadas por fecha
    consultas = Consulta.objects.all().order_by('-fecha')
    
    # Añadir datos de APIs veterinarias
    api_data = {
        'nearby_clinics': [],
        'emergency_clinics': [],
        'health_tips': []
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

# =============================================
# VISTA PARA CREAR: Nueva consulta médica
# =============================================
@login_required
def crear_consulta(request):
    # Si el usuario envía el formulario
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()  # Guardamos la consulta en la base de datos
            
            # Enviamos notificación por WebSocket
            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'clinica_notificaciones',
                    {
                        'type': 'enviar.notificacion',
                        'message': '¡Nueva consulta médica creada!'
                    }
                )
            except:
                # Si Redis no funciona, la web sigue funcionando
                pass
            
            # Mensaje de éxito para el usuario
            messages.success(request, 'Consulta creada correctamente')
            return redirect('lista_consultas')
    else:
        # Mostramos el formulario vacío
        form = ConsultaForm()
    
    # Usamos plantilla genérica
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Nueva Consulta Médica',
        'url_cancelar': '/consultas/'
    })

# =============================================
# VISTA PARA ACTUALIZAR: Cambiar estado de la consulta
# =============================================
@login_required
def actualizar_estado_consulta(request, id):
    # Solo usuarios con permiso de cambiar consultas pueden modificar el estado
    if not request.user.has_perm('consultas.change_consulta'):
        messages.error(request, 'No tienes permisos para cambiar estados')
        return redirect('lista_consultas')

    # Si recibimos el formulario con el nuevo estado
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')  # Recibimos el nuevo estado
        
        # Usamos get_object_or_404 para evitar errores 500 si el ID no existe
        consulta = get_object_or_404(Consulta, id=id)     # Buscamos la consulta
        consulta.estado = nuevo_estado                      # Cambiamos el estado
        consulta.save()                                     # Guardamos en la BD

        # Enviamos notificación por WebSocket
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'clinica_notificaciones',
                {
                    'type': 'enviar.notificacion',
                    'message': f'El estado de la consulta cambió a: {nuevo_estado}'
                }
            )
        except:
            # Si Redis no funciona, la web sigue funcionando
            pass
        
        # Mensaje de éxito para el usuario
        messages.success(request, f'Estado actualizado a: {nuevo_estado}')
        
    return redirect('lista_consultas')

# =============================================
# VISTA PARA EDITAR: Modificar consulta completa
# =============================================
@login_required
def editar_consulta(request, id):
    # Solo usuarios con permiso pueden editar
    if not request.user.has_perm('consultas.change_consulta'):
        messages.error(request, 'No tienes permisos para editar consultas')
        return redirect('lista_consultas')
    
    consulta = get_object_or_404(Consulta, id=id)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta actualizada correctamente')
            return redirect('lista_consultas')
    else:
        form = ConsultaForm(instance=consulta)
    
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Editar Consulta',
        'url_cancelar': '/consultas/'
    })

# =============================================
# VISTA PARA ELIMINAR: Borrar consulta
# =============================================
@login_required
def eliminar_consulta(request, id):
    # Solo usuarios con permiso pueden eliminar
    if not request.user.has_perm('consultas.delete_consulta'):
        messages.error(request, 'No tienes permisos para eliminar consultas')
        return redirect('lista_consultas')
    
    consulta = get_object_or_404(Consulta, id=id)
    
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'Consulta eliminada correctamente')
        return redirect('lista_consultas')
    
    # GET: mostrar confirmación
    return render(request, 'confirmar_eliminar.html', {
        'objeto': consulta,
        'titulo': 'Eliminar Consulta',
        'url_cancelar': '/consultas/'
    })

# =============================================
# FUNCIONALIDADES DE APIs INTEGRADAS EN VISTAS EXISTENTES
# =============================================

@login_required
def api_clinics_cercanas(request):
    """API endpoint para obtener clínicas cercanas (AJAX)"""
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
