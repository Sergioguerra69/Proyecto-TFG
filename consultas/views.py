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
import json
from django.views.decorators.csrf import csrf_exempt

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
    # Comprobar si el usuario es recepcionista, veterinario o admin
    es_personal = request.user.is_staff or request.user.is_superuser
    if hasattr(request.user, 'perfil') and request.user.perfil.rol in ['recepcionista', 'admin', 'veterinario']:
        es_personal = True

    if es_personal:
        consultas = Consulta.objects.all().order_by('-fecha')
    else:
        consultas = Consulta.objects.filter(usuario=request.user).order_by('-fecha')
    
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
            
    return render(request, 'consultas/consultas.html', {
        'consultas': consultas,
        'api_data': api_data,
        'api_available': API_AVAILABLE
    })

# VER DETALLE DE CONSULTA - Información completa de la cita
@login_required
def detalle_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    return render(request, 'consultas/detalle_consulta.html', {
        'consulta': consulta
    })

# CREAR NUEVA CONSULTA - Cuando un cliente pide cita
@login_required
def crear_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST, user=request.user)
        if form.is_valid():
            consulta = form.save(commit=False)  # Guardamos pero sin confirmar aún
            if consulta.mascota and not consulta.paciente:
                consulta.paciente = consulta.mascota.nombre
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
            return redirect('calendario_recepcion')
    else:
        form = ConsultaForm(user=request.user)
    
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Pedir Nueva Consulta Veterinaria',
        'url_cancelar': '/consultas/calendario/'
    })

# CAMBIAR ESTADO - Actualizar cómo va la consulta
@login_required
def actualizar_estado_consulta(request, id):
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
        
    return redirect('calendario_recepcion')

# EDITAR CONSULTA - Cambiar datos de una cita
@login_required
def editar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta, user=request.user)
        if form.is_valid():
            c = form.save(commit=False)
            if c.mascota and not c.paciente:
                c.paciente = c.mascota.nombre
            c.save()
            messages.success(request, '¡Consulta actualizada!')
            return redirect('calendario_recepcion')
    else:
        form = ConsultaForm(instance=consulta, user=request.user)
    
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Editar Datos de la Consulta',
        'url_cancelar': '/consultas/calendario/'
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

# --- CALENDARIO INTERACTIVO ---

@login_required
def calendario_recepcion(request):
    # comprobar si el usuario es empleado (recepcionista, admin, veterinario, auxiliar)
    es_empleado = request.user.is_staff or request.user.is_superuser
    if hasattr(request.user, 'perfil') and request.user.perfil.rol in ['recepcionista', 'admin', 'veterinario', 'auxiliar']:
        es_empleado = True

    titulo = 'Calendario General de Citas' if es_empleado else 'Mi Calendario de Citas'
    return render(request, 'consultas/calendario.html', {
        'titulo': titulo,
        'es_empleado': es_empleado
    })

@login_required
def api_citas_calendario(request):
    # comprobar si el usuario es empleado o cliente
    es_empleado = request.user.is_staff or request.user.is_superuser
    if hasattr(request.user, 'perfil') and request.user.perfil.rol in ['recepcionista', 'admin', 'veterinario', 'auxiliar']:
        es_empleado = True

    eventos = []
    from datetime import timedelta, datetime

    # 1. CONSULTAS
    if es_empleado:
        consultas = Consulta.objects.all()
    else:
        consultas = Consulta.objects.filter(usuario=request.user)

    for c in consultas:
        color = '#0891b2' # cian por defecto
        if c.estado == 'Pendiente':
            color = '#f59e0b' # amarillo
        elif c.estado == 'En Proceso':
            color = '#0ea5e9' # azul
        elif c.estado == 'Completado':
            color = '#10b981' # verde
        elif c.estado == 'Rechazada':
            color = '#ef4444' # rojo
            
        end_time = c.fecha + timedelta(minutes=30)
        nombre_paciente = c.mascota.nombre if c.mascota else c.paciente
        titulo_evento = f'[Consulta] {nombre_paciente} ({c.usuario.username})' if es_empleado else f'[Consulta] {nombre_paciente} - {c.motivo}'

        eventos.append({
            'id': c.id,
            'title': titulo_evento,
            'start': c.fecha.isoformat(),
            'end': end_time.isoformat(),
            'backgroundColor': color,
            'borderColor': color,
            'url': f'/consultas/editar/{c.id}/',
        })

    # 2. CIRUGÍAS
    from cirugias.models import Cirugia
    if es_empleado:
        cirugias = Cirugia.objects.all()
    else:
        cirugias = Cirugia.objects.filter(usuario=request.user)

    for ci in cirugias:
        color = '#8b5cf6' # morado para cirugías
        end_time = ci.fecha + timedelta(minutes=60)
        titulo_evento = f'[Cirugía] {ci.paciente} - {ci.tipo_cirugia}'
        eventos.append({
            'id': f'cirugia_{ci.id}',
            'title': titulo_evento,
            'start': ci.fecha.isoformat(),
            'end': end_time.isoformat(),
            'backgroundColor': color,
            'borderColor': color,
            'url': f'/notificaciones/ver/cirugia/{ci.id}/' if es_empleado else '',
        })

    # 3. ESTÉTICA
    from estetica.models import ServicioEstetica
    if es_empleado:
        esteticas = ServicioEstetica.objects.all()
    else:
        esteticas = ServicioEstetica.objects.filter(usuario=request.user)

    for es in esteticas:
        color = '#ec4899' # rosa para estética
        end_time = es.fecha + timedelta(minutes=45)
        titulo_evento = f'[Estética] {es.paciente} - {es.tipo_servicio}'
        eventos.append({
            'id': f'estetica_{es.id}',
            'title': titulo_evento,
            'start': es.fecha.isoformat(),
            'end': end_time.isoformat(),
            'backgroundColor': color,
            'borderColor': color,
            'url': f'/notificaciones/ver/estetica/{es.id}/' if es_empleado else '',
        })

    # 4. ANÁLISIS
    from laboratorio.models import Analisis
    if es_empleado:
        analisis = Analisis.objects.all()
    else:
        analisis = Analisis.objects.filter(usuario=request.user)

    for an in analisis:
        color = '#059669' # verde oscuro para laboratorio
        if an.hora:
            dt_start = datetime.combine(an.fecha, an.hora)
            end_time = dt_start + timedelta(minutes=30)
            titulo_evento = f'[Análisis] {an.paciente} - {an.nombre}'
            eventos.append({
                'id': f'analisis_{an.id}',
                'title': titulo_evento,
                'start': dt_start.isoformat(),
                'end': end_time.isoformat(),
                'backgroundColor': color,
                'borderColor': color,
                'url': f'/notificaciones/ver/analisis/{an.id}/' if es_empleado else '',
            })

    # 5. FORMULARIOS DE CONTACTO
    from contacto.models import FormularioContacto
    if es_empleado:
        contactos = FormularioContacto.objects.all()
    else:
        contactos = FormularioContacto.objects.filter(usuario=request.user)

    for co in contactos:
        color = '#f97316' # naranja para contacto
        if co.hora:
            dt_start = datetime.combine(co.fecha, co.hora)
            end_time = dt_start + timedelta(minutes=30)
            titulo_evento = f'[Contacto] {co.nombre} {co.apellidos} - {co.asunto}'
            eventos.append({
                'id': f'contacto_{co.id}',
                'title': titulo_evento,
                'start': dt_start.isoformat(),
                'end': end_time.isoformat(),
                'backgroundColor': color,
                'borderColor': color,
                'url': f'/contacto/ver/{co.id}/' if es_empleado else '',
            })

    return JsonResponse(eventos, safe=False)

@csrf_exempt
@login_required
def api_actualizar_cita(request, id):
    # actualizar fecha de la cita tras moverla en el calendario
    if request.method == 'POST':
        try:
            # verificar si tiene permiso para mover citas (solo empleados)
            es_empleado = request.user.is_staff or request.user.is_superuser
            if hasattr(request.user, 'perfil') and request.user.perfil.rol in ['recepcionista', 'admin', 'veterinario', 'auxiliar']:
                es_empleado = True

            if not es_empleado:
                return JsonResponse({'success': False, 'error': 'Solo el personal de recepción puede reubicar citas en el calendario'})

            data = json.loads(request.body)
            nueva_fecha_str = data.get('start')
            
            if nueva_fecha_str:
                from dateutil.parser import parse
                nueva_fecha = parse(nueva_fecha_str)
                
                consulta = get_object_or_404(Consulta, id=id)
                consulta.fecha = nueva_fecha
                consulta.save()
                
                return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
