# Sistema de notificaciones de la clínica veterinaria
# Aquí gestionamos todos los mensajes internos entre el personal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import Notificacion
from consultas.models import Consulta
from laboratorio.models import Analisis
from cirugias.models import Cirugia
from urgencias.models import Urgencia

# PANEL DE RECEPCIÓN: Aquí llegan todas las solicitudes nuevas
@login_required
def panel_recepcion(request):
    # Separamos las consultas por estado
    consultas_pendientes = Consulta.objects.filter(estado='Pendiente').order_by('-fecha')
    consultas_aceptadas = Consulta.objects.filter(estado='Aceptada').order_by('-fecha')
    consultas_rechazadas = Consulta.objects.filter(estado='Rechazada').order_by('-fecha')
    
    # Lo mismo para otros servicios
    analisis_pendientes = Analisis.objects.filter(estado='Pendiente').order_by('-fecha')
    analisis_aceptados = Analisis.objects.filter(estado='Aceptada').order_by('-fecha')
    analisis_rechazados = Analisis.objects.filter(estado='Rechazada').order_by('-fecha')
    
    cirugias_pendientes = Cirugia.objects.filter(estado='Pendiente').order_by('-fecha')
    cirugias_aceptadas = Cirugia.objects.filter(estado='Aceptada').order_by('-fecha')
    cirugias_rechazadas = Cirugia.objects.filter(estado='Rechazada').order_by('-fecha')
    
    urgencias_pendientes = Urgencia.objects.filter(estado='Pendiente').order_by('-fecha')
    urgencias_aceptadas = Urgencia.objects.filter(estado='Aceptada').order_by('-fecha')
    urgencias_rechazadas = Urgencia.objects.filter(estado='Rechazada').order_by('-fecha')
    
    # Notificaciones recientes PENDIENTES para el recepcionista
    # Solo mostramos notificaciones de citas que están en estado 'Pendiente'
    notificaciones_recientes = Notificacion.objects.filter(
        receptor=request.user,
        estado='pendiente'
    ).order_by('-fecha_creacion')[:10]
    
    # Contador de notificaciones pendientes
    notificaciones_pendientes_count = Notificacion.objects.filter(
        receptor=request.user,
        estado='pendiente'
    ).count()
    
    # Mostramos todo organizado por estado en el panel de recepción
    return render(request, 'notificaciones/panel_recepcion.html', {
        # Consultas separadas por estado
        'consultas_pendientes': consultas_pendientes,
        'consultas_aceptadas': consultas_aceptadas,
        'consultas_rechazadas': consultas_rechazadas,
        
        # Análisis separados por estado
        'analisis_pendientes': analisis_pendientes,
        'analisis_aceptados': analisis_aceptados,
        'analisis_rechazados': analisis_rechazados,
        
        # Cirugías separadas por estado
        'cirugias_pendientes': cirugias_pendientes,
        'cirugias_aceptadas': cirugias_aceptadas,
        'cirugias_rechazadas': cirugias_rechazadas,
        
        # Urgencias separadas por estado
        'urgencias_pendientes': urgencias_pendientes,
        'urgencias_aceptadas': urgencias_aceptadas,
        'urgencias_rechazadas': urgencias_rechazadas,
        
        # Notificaciones del recepcionista
        'notificaciones_recientes': notificaciones_recientes,
        'notificaciones_pendientes_count': notificaciones_pendientes_count,
    })

# ACEPTAR SOLICITUD: Cuando el recepcionista aprueba una cita
@login_required
def aceptar_solicitud(request, notificacion_id):
    # Buscamos la notificación que queremos aceptar
    notificacion = get_object_or_404(Notificacion, id=notificacion_id)
    
    # Cambiamos el estado de la cita/consulta a "Aceptada"
    objeto = notificacion.get_objeto()
    if objeto:
        objeto.estado = 'Aceptada'  # La cita ha sido aprobada por recepción
        objeto.save()
    
    # Marcamos la notificación original como aceptada
    notificacion.estado = 'aceptada'
    notificacion.save()
    
    # Creamos notificación para todos los veterinarios
    veterinarios = User.objects.filter(groups__name='Veterinarios')
    for vet in veterinarios:
        Notificacion.objects.create(
            tipo=notificacion.tipo,
            objeto_id=notificacion.objeto_id,
            emisor=request.user,
            receptor=vet,
            estado='pendiente'
        )
    
    # Notificación en tiempo real a veterinarios
    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'clinica_notificaciones',
            {
                'type': 'enviar.notificacion',
                'message': f'Consulta de {objeto.paciente} aceptada - asignada a veterinarios'
            }
        )
    except:
        pass
    
    messages.success(request, 'Consulta aceptada y notificada a veterinarios')
    return redirect('panel_recepcion')

# RECHAZAR SOLICITUD: Cuando no podemos atender una cita
@login_required
def rechazar_solicitud(request, notificacion_id):
    # Buscamos la notificación que vamos a rechazar
    notificacion = get_object_or_404(Notificacion, id=notificacion_id)
    
    # Cambiamos el estado de la cita a "Rechazada"
    objeto = notificacion.get_objeto()
    if objeto:
        objeto.estado = 'Rechazada'  # La cita ha sido rechazada por recepción
        objeto.save()
    
    # Marcamos la notificación como rechazada
    notificacion.estado = 'rechazada'
    notificacion.save()
    
    # Notificación en tiempo real
    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'clinica_notificaciones',
            {
                'type': 'enviar.notificacion',
                'message': f'Consulta de {objeto.paciente} ha sido rechazada'
            }
        )
    except:
        pass
    
    messages.success(request, 'Consulta rechazada correctamente')
    return redirect('panel_recepcion')

# PANEL VETERINARIO: Aquí los veterinarios ven sus tareas
@login_required
def panel_veterinario(request):
    # Separamos las notificaciones por estado
    notificaciones_pendientes = Notificacion.objects.filter(
        receptor=request.user,
        estado='pendiente'
    ).order_by('-fecha_creacion')
    
    notificaciones_aceptadas = Notificacion.objects.filter(
        receptor=request.user,
        estado='aceptada'
    ).order_by('-fecha_creacion')
    
    notificaciones_rechazadas = Notificacion.objects.filter(
        receptor=request.user,
        estado='rechazada'
    ).order_by('-fecha_creacion')
    
    # Contador de notificaciones pendientes
    notificaciones_pendientes_count = notificaciones_pendientes.count()
    
    # Mostramos las notificaciones organizadas por estado
    return render(request, 'notificaciones/panel_veterinario.html', {
        'notificaciones_pendientes': notificaciones_pendientes,
        'notificaciones_aceptadas': notificaciones_aceptadas,
        'notificaciones_rechazadas': notificaciones_rechazadas,
        'notificaciones_pendientes_count': notificaciones_pendientes_count,
    })

# MIS NOTIFICACIONES: Lista de mensajes para el veterinario
@login_required
def mis_notificaciones(request):
    # Sacamos todas las notificaciones que son para este veterinario
    notificaciones = Notificacion.objects.filter(
        receptor=request.user
    ).order_by('-fecha_creacion')
    
    return render(request, 'notificaciones/mis_notificaciones.html', {
        'notificaciones': notificaciones,
    })



# Aceptar cita - El veterinario la pone en proceso
@login_required
def aceptar_cita(request, tipo, cita_id):
    # Obtener el objeto según el tipo
    if tipo == 'consulta':
        objeto = get_object_or_404(Consulta, id=cita_id)
    elif tipo == 'analisis':
        objeto = get_object_or_404(Analisis, id=cita_id)
    elif tipo == 'cirugia':
        objeto = get_object_or_404(Cirugia, id=cita_id)
    elif tipo == 'urgencia':
        objeto = get_object_or_404(Urgencia, id=cita_id)
    else:
        messages.error(request, 'Tipo de cita no válido')
        return redirect('panel_recepcion')
    
    # Cambiar estado a Aceptada
    objeto.estado = 'Aceptada'
    objeto.save()
    
    # Buscar y actualizar la notificación del recepcionista
    notificacion = Notificacion.objects.filter(
        tipo=tipo,
        objeto_id=cita_id,
        receptor=request.user
    ).first()
    
    if notificacion:
        notificacion.estado = 'aceptada'
        notificacion.save()
    
    # El veterinario ha aceptado la cita - fin del flujo de notificaciones
    # No se crean nuevas notificaciones, la cita está asignada al veterinario
    
    messages.success(request, f'{tipo.title()} aceptada correctamente. La cita ha sido asignada a ti.')
    return redirect('panel_recepcion')

# Rechazar cita - Se cancela la cita
@login_required
def rechazar_cita(request, tipo, cita_id):
    # Obtener el objeto según el tipo
    if tipo == 'consulta':
        objeto = get_object_or_404(Consulta, id=cita_id)
    elif tipo == 'analisis':
        objeto = get_object_or_404(Analisis, id=cita_id)
    elif tipo == 'cirugia':
        objeto = get_object_or_404(Cirugia, id=cita_id)
    elif tipo == 'urgencia':
        objeto = get_object_or_404(Urgencia, id=cita_id)
    else:
        messages.error(request, 'Tipo de cita no válido')
        return redirect('panel_recepcion')
    
    # Cambiar estado a Rechazada
    objeto.estado = 'Rechazada'
    objeto.save()
    
    # Buscar y actualizar la notificación del recepcionista
    notificacion = Notificacion.objects.filter(
        tipo=tipo,
        objeto_id=cita_id,
        receptor=request.user
    ).first()
    
    if notificacion:
        notificacion.estado = 'rechazada'
        notificacion.save()
    
    messages.success(request, f'{tipo.title()} rechazada correctamente')
    return redirect('panel_recepcion')

# Cancelar cita aceptada - Vuelve a estado Pendiente
@login_required
def cancelar_cita(request, tipo, cita_id):
    # Obtener el objeto según el tipo
    if tipo == 'consulta':
        objeto = get_object_or_404(Consulta, id=cita_id)
    elif tipo == 'analisis':
        objeto = get_object_or_404(Analisis, id=cita_id)
    elif tipo == 'cirugia':
        objeto = get_object_or_404(Cirugia, id=cita_id)
    elif tipo == 'urgencia':
        objeto = get_object_or_404(Urgencia, id=cita_id)
    else:
        messages.error(request, 'Tipo de cita no válido')
        return redirect('panel_recepcion')
    
    # Cambiar estado a Pendiente (cancela la aceptación)
    objeto.estado = 'Pendiente'
    objeto.save()
    
    # Buscar y actualizar la notificación del veterinario a pendiente
    notificacion = Notificacion.objects.filter(
        tipo=tipo,
        objeto_id=cita_id,
        receptor=request.user,
        estado='aceptada'
    ).first()
    
    if notificacion:
        notificacion.estado = 'pendiente'
        notificacion.save()
    
    messages.success(request, f'{tipo.title()} cancelada. Vuelve a estar pendiente de asignación.')
    return redirect('panel_veterinario')

# Eliminar cita - Se borra completamente
@login_required
def eliminar_cita(request, tipo, cita_id):
    # Obtener el objeto según el tipo
    if tipo == 'consulta':
        objeto = get_object_or_404(Consulta, id=cita_id)
    elif tipo == 'analisis':
        objeto = get_object_or_404(Analisis, id=cita_id)
    elif tipo == 'cirugia':
        objeto = get_object_or_404(Cirugia, id=cita_id)
    elif tipo == 'urgencia':
        objeto = get_object_or_404(Urgencia, id=cita_id)
    else:
        messages.error(request, 'Tipo de cita no válido')
        return redirect('panel_recepcion')
    
    # Eliminar objeto
    objeto.delete()
    
    messages.success(request, f'{tipo.title()} eliminada correctamente')
    return redirect('panel_recepcion')

# Ver detalles de una cita - Muestra toda la información del formulario
@login_required
def ver_cita(request, tipo, cita_id):
    # Obtener el objeto según el tipo
    if tipo == 'consulta':
        objeto = get_object_or_404(Consulta, id=cita_id)
    elif tipo == 'analisis':
        from laboratorio.models import Analisis
        objeto = get_object_or_404(Analisis, id=cita_id)
    elif tipo == 'cirugia':
        from cirugias.models import Cirugia
        objeto = get_object_or_404(Cirugia, id=cita_id)
    elif tipo == 'urgencia':
        from urgencias.models import Urgencia
        objeto = get_object_or_404(Urgencia, id=cita_id)
    else:
        messages.error(request, 'Tipo de cita no válido')
        return redirect('panel_recepcion')
    
    return render(request, 'notificaciones/ver_cita.html', {
        'tipo': tipo,
        'cita': objeto,
    })

# Crear nueva cita - Formulario para añadir solicitudes
@login_required
def crear_cita(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        paciente = request.POST.get('paciente')
        fecha = request.POST.get('fecha')
        motivo = request.POST.get('motivo')
        
        # Crear objeto según el tipo
        if tipo == 'consulta':
            cita = Consulta.objects.create(
                paciente=paciente,
                fecha=fecha,
                motivo=motivo,
                estado='Pendiente'
            )
        elif tipo == 'analisis':
            cita = Analisis.objects.create(
                paciente=paciente,
                fecha=fecha,
                tipo=motivo,  # Para análisis, el motivo es el tipo
                estado='Pendiente'
            )
        elif tipo == 'cirugia':
            cita = Cirugia.objects.create(
                paciente=paciente,
                fecha=fecha,
                tipo=motivo,  # Para cirugías, el motivo es el tipo
                estado='Pendiente'
            )
        elif tipo == 'urgencia':
            cita = Urgencia.objects.create(
                paciente=paciente,
                fecha=fecha,
                motivo=motivo,
                estado='Pendiente'
            )
        else:
            messages.error(request, 'Tipo de cita no válido')
            return redirect('panel_recepcion')
        
        # Crear notificación para recepcionistas
        recepcionistas = User.objects.filter(groups__name='Recepcionistas')
        for recep in recepcionistas:
            Notificacion.objects.create(
                tipo=tipo,
                objeto_id=cita.id,
                emisor=request.user,
                receptor=recep,
                estado='pendiente'
            )
        
        messages.success(request, f'{tipo.title()} creada correctamente')
        return redirect('panel_recepcion')
    
    return redirect('panel_recepcion')

# Configurar permisos - Solo para administradores
@login_required
def configurar_permisos(request):
    # Solo administradores pueden acceder
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para configurar usuarios')
        return redirect('home')
    
    if request.method == 'POST':
        # Obtener grupos
        veterinarios_group = Group.objects.get_or_create(name='veterinarios')[0]
        recepcionistas_group = Group.objects.get_or_create(name='recepcionistas')[0]
        
        # Limpiar grupos existentes
        veterinarios_group.user_set.clear()
        recepcionistas_group.user_set.clear()
        
        # Asignar usuarios según el formulario
        for key, value in request.POST.items():
            if key.startswith('veterinario_') and value == 'on':
                user_id = key.replace('veterinario_', '')
                try:
                    user = User.objects.get(id=user_id)
                    veterinarios_group.user_set.add(user)
                except User.DoesNotExist:
                    continue
            
            if key.startswith('recepcionista_') and value == 'on':
                user_id = key.replace('recepcionista_', '')
                try:
                    user = User.objects.get(id=user_id)
                    recepcionistas_group.user_set.add(user)
                except User.DoesNotExist:
                    continue
        
        messages.success(request, 'Permisos configurados correctamente')
        return redirect('configurar_permisos')
    
    # Obtener todos los usuarios y grupos actuales
    usuarios = User.objects.all()
    veterinarios_group = Group.objects.filter(name='veterinarios').first()
    recepcionistas_group = Group.objects.filter(name='recepcionistas').first()
    
    veterinarios_ids = []
    recepcionistas_ids = []
    
    if veterinarios_group:
        veterinarios_ids = veterinarios_group.user_set.values_list('id', flat=True)
    if recepcionistas_group:
        recepcionistas_ids = recepcionistas_group.user_set.values_list('id', flat=True)
    
    return render(request, 'notificaciones/configurar_permisos.html', {
        'usuarios': usuarios,
        'veterinarios_ids': veterinarios_ids,
        'recepcionistas_ids': recepcionistas_ids,
    })

def crear_notificacion_automatica(tipo, objeto_id, emisor, receptor):
    """Crea una notificación cuando un cliente pide algo"""
    Notificacion.objects.create(
        tipo=tipo,
        objeto_id=objeto_id,
        emisor=emisor,
        receptor=receptor,
        estado='pendiente'
    )

# VISTAS SIMPLIFICADAS PARA EL PANEL DE RECEPCIÓN
# Estas vistas permiten aceptar/rechazar sin depender de notificaciones

@login_required
def aceptar_cita_recepcion(request, tipo, cita_id):
    """Aceptar una cita directamente desde el panel de recepción"""
    # Buscar el objeto según el tipo
    if tipo == 'consulta':
        objeto = get_object_or_404(Consulta, id=cita_id)
    elif tipo == 'analisis':
        from laboratorio.models import Analisis
        objeto = get_object_or_404(Analisis, id=cita_id)
    elif tipo == 'cirugia':
        from cirugias.models import Cirugia
        objeto = get_object_or_404(Cirugia, id=cita_id)
    elif tipo == 'urgencia':
        from urgencias.models import Urgencia
        objeto = get_object_or_404(Urgencia, id=cita_id)
    else:
        messages.error(request, 'Tipo de cita no válido')
        return redirect('panel_recepcion')
    
    # Cambiar estado a Aceptada
    objeto.estado = 'Aceptada'
    objeto.save()
    
    # Actualizar la notificación del recepcionista a 'aceptada'
    notificacion = Notificacion.objects.filter(
        tipo=tipo,
        objeto_id=cita_id,
        receptor=request.user,
        estado='pendiente'
    ).first()
    
    if notificacion:
        notificacion.estado = 'aceptada'
        notificacion.save()
    
    # Notificar a veterinarios
    veterinarios = User.objects.filter(groups__name='Veterinarios')
    for vet in veterinarios:
        Notificacion.objects.create(
            tipo=tipo,
            objeto_id=cita_id,
            emisor=request.user,
            receptor=vet,
            estado='pendiente'
        )
    
    messages.success(request, f'{tipo.capitalize()} aceptada correctamente')
    return redirect('panel_recepcion')

@login_required
def rechazar_cita_recepcion(request, tipo, cita_id):
    """Rechazar una cita directamente desde el panel de recepción"""
    # Buscar el objeto según el tipo
    if tipo == 'consulta':
        objeto = get_object_or_404(Consulta, id=cita_id)
    elif tipo == 'analisis':
        from laboratorio.models import Analisis
        objeto = get_object_or_404(Analisis, id=cita_id)
    elif tipo == 'cirugia':
        from cirugias.models import Cirugia
        objeto = get_object_or_404(Cirugia, id=cita_id)
    elif tipo == 'urgencia':
        from urgencias.models import Urgencia
        objeto = get_object_or_404(Urgencia, id=cita_id)
    else:
        messages.error(request, 'Tipo de cita no válido')
        return redirect('panel_recepcion')
    
    # Cambiar estado a Rechazada
    objeto.estado = 'Rechazada'
    objeto.save()
    
    # Actualizar la notificación a 'rechazada'
    notificacion = Notificacion.objects.filter(
        tipo=tipo,
        objeto_id=cita_id,
        receptor=request.user,
        estado='pendiente'
    ).first()
    
    if notificacion:
        notificacion.estado = 'rechazada'
        notificacion.save()
    
    messages.success(request, f'{tipo.capitalize()} rechazada correctamente')
    return redirect('panel_recepcion')
