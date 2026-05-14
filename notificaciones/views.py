# Sistema de notificaciones de la clínica veterinaria
# Aquí gestionamos todos los mensajes internos entre el personal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import Notificacion

# Importaciones de modelos usados en varias vistas
try:
    from consultas.models import Consulta
except ImportError:
    Consulta = None
try:
    from laboratorio.models import Analisis
except ImportError:
    Analisis = None
try:
    from cirugias.models import Cirugia
except ImportError:
    Cirugia = None
try:
    from urgencias.models import Urgencia
except ImportError:
    Urgencia = None
try:
    from contacto.models import FormularioContacto, MensajeCliente
except ImportError:
    FormularioContacto = None
    MensajeCliente = None

# PANEL DE RECEPCIÓN: Aquí llegan todas las solicitudes nuevas
@login_required
def panel_recepcion(request):
    # Verificar si es recepcionista
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    # Cargar los modelos, si no existen, mostrar listas vacías
    if Consulta:
        consultas_pendientes = Consulta.objects.filter(estado='Pendiente').order_by('-fecha')
        consultas_aceptadas = Consulta.objects.filter(estado='Aceptada').order_by('-fecha')
        consultas_rechazadas = Consulta.objects.filter(estado='Rechazada').order_by('-fecha')
    else:
        consultas_pendientes = consultas_aceptadas = consultas_rechazadas = []

    if Analisis:
        analisis_pendientes = Analisis.objects.filter(estado='Pendiente').order_by('-fecha')
        analisis_aceptados = Analisis.objects.filter(estado='Aceptada').order_by('-fecha')
        analisis_rechazados = Analisis.objects.filter(estado='Rechazado').order_by('-fecha')
    else:
        analisis_pendientes = analisis_aceptados = analisis_rechazados = []

    if Cirugia:
        cirugias_pendientes = Cirugia.objects.filter(estado='Pendiente').order_by('-fecha')
        cirugias_aceptadas = Cirugia.objects.filter(estado='Aceptada').order_by('-fecha')
        cirugias_rechazadas = Cirugia.objects.filter(estado='Rechazada').order_by('-fecha')
    else:
        cirugias_pendientes = cirugias_aceptadas = cirugias_rechazadas = []

    if Urgencia:
        urgencias_pendientes = Urgencia.objects.filter(estado='Pendiente').order_by('-fecha')
        urgencias_aceptadas = Urgencia.objects.filter(estado='Aceptada').order_by('-fecha')
        urgencias_rechazadas = Urgencia.objects.filter(estado='Rechazada').order_by('-fecha')
    else:
        urgencias_pendientes = urgencias_aceptadas = urgencias_rechazadas = []
    
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
    
    contactos_pendientes = FormularioContacto.objects.filter(estado='Pendiente').order_by('-fecha_creacion')
    contactos_aceptados = FormularioContacto.objects.filter(estado='Respondido').order_by('-fecha_creacion')
    contactos_rechazados = FormularioContacto.objects.filter(estado='Cancelado').order_by('-fecha_creacion')
    
    # Dudas (MensajeCliente)
    dudas_pendientes = MensajeCliente.objects.filter(estado='Pendiente').order_by('-fecha_creacion')
    dudas_leidas = MensajeCliente.objects.filter(estado='Leído').order_by('-fecha_creacion')
    
    # Contador de notificaciones de contacto pendientes (sigue siendo útil para insignias si se desea)
    contactos_pendientes_count = contactos_pendientes.count() + dudas_pendientes.count()
    
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
        
        # Formularios de contacto separados por estado
        'contactos_pendientes': contactos_pendientes,
        'contactos_aceptados': contactos_aceptados,
        'contactos_rechazados': contactos_rechazados,
        'contactos_pendientes_count': contactos_pendientes_count,
        
        # Dudas
        'dudas_pendientes': dudas_pendientes,
        'dudas_leidas': dudas_leidas,
        
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
        if notificacion.tipo == 'formulario_contacto':
            objeto.estado = 'Respondido'
        elif notificacion.tipo == 'mensaje_contacto':
            objeto.estado = 'Leído'
        else:
            objeto.estado = 'Aceptada'
        objeto.save()
    
    # Marcamos la notificación original como aceptada
    notificacion.estado = 'aceptada'
    notificacion.save()
    
    # Creamos notificación para todos los veterinarios (por rol de perfil)
    veterinarios = User.objects.filter(perfil__rol='veterinario')
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
        if notificacion.tipo == 'formulario_contacto':
            objeto.estado = 'Cancelado'
        elif notificacion.tipo == 'mensaje_contacto':
            objeto.estado = 'Leído'
        else:
            objeto.estado = 'Rechazada'
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
    # Verificar si es veterinario
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'veterinario'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    # Separamos las notificaciones por estado
    notificaciones_pendientes_qs = Notificacion.objects.filter(
        receptor=request.user,
        estado='pendiente'
    ).order_by('-fecha_creacion')
    
    notificaciones_aceptadas_qs = Notificacion.objects.filter(
        receptor=request.user,
        estado='aceptada'
    ).order_by('-fecha_creacion')
    
    notificaciones_rechazadas_qs = Notificacion.objects.filter(
        receptor=request.user,
        estado='rechazada'
    ).order_by('-fecha_creacion')
    
    def enriquecer(notifs):
        """Añade el objeto cita real a cada notificación para la plantilla."""
        resultado = []
        for notif in notifs:
            cita = notif.get_objeto()
            resultado.append({
                'notif': notif,
                'cita': cita,
                'tipo': notif.tipo,
                'tipo_display': notif.get_tipo_display(),
                'estado': notif.estado,
                'fecha_notif': notif.fecha_creacion,
                'emisor': notif.emisor,
                'objeto_id': notif.objeto_id,
                # Campos comunes del objeto (mapeados según el tipo)
                'paciente': (getattr(cita, 'paciente', None) or getattr(cita, 'nombre', '-')) if cita else '-',
                'fecha_cita': (getattr(cita, 'fecha', None) or getattr(cita, 'fecha_creacion', None)) if cita else None,
                'detalle': (getattr(cita, 'motivo', None) or getattr(cita, 'asunto', '-')) if cita else '-',
            })
        return resultado
    
    # Contador de notificaciones pendientes
    notificaciones_pendientes_count = notificaciones_pendientes_qs.count()
    
    # Mostramos las notificaciones organizadas por estado, enriquecidas con datos de la cita
    return render(request, 'notificaciones/panel_veterinario.html', {
        'notificaciones_pendientes': enriquecer(notificaciones_pendientes_qs),
        'notificaciones_aceptadas': enriquecer(notificaciones_aceptadas_qs),
        'notificaciones_rechazadas': enriquecer(notificaciones_rechazadas_qs),
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



# ---------- Helper WebSocket ----------
def _ws_send(group, event_type, payload):
    """Envía un evento por channel layer de forma síncrona. Silencia errores si no hay WS."""
    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(group, {"type": event_type, **payload})
    except Exception:
        pass


# Aceptar cita - Comportamiento diferente según el rol
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
    elif tipo == 'formulario_contacto':
        objeto = get_object_or_404(FormularioContacto, id=cita_id)
    elif tipo == 'mensaje_contacto':
        objeto = get_object_or_404(MensajeCliente, id=cita_id)
    else:
        messages.error(request, 'Tipo de cita no válido')
        return redirect('panel_recepcion')
    
    es_recepcionista = (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista') or request.user.is_staff
    
    if es_recepcionista:
        # --- FLUJO RECEPCIONISTA ---
        # Cambia la cita a Aceptada y notifica a todos los veterinarios
        objeto.estado = 'Aceptada'
        objeto.save()
        
        # Marcar la notificación propia del recepcionista como aceptada
        notif_recep = Notificacion.objects.filter(
            tipo=tipo, objeto_id=cita_id, receptor=request.user
        ).first()
        if notif_recep:
            notif_recep.estado = 'aceptada'
            notif_recep.save()
        
        # Crear notificación pendiente para TODOS los veterinarios (por rol de perfil)
        veterinarios = User.objects.filter(perfil__rol='veterinario')
        for vet in veterinarios:
            # Evitar duplicados: solo crear si no existe ya una notif pendiente para ese vet+cita
            ya_existe = Notificacion.objects.filter(
                tipo=tipo,
                objeto_id=cita_id,
                receptor=vet,
                estado='pendiente'
            ).exists()
            if not ya_existe:
                Notificacion.objects.create(
                    tipo=tipo,
                    objeto_id=cita_id,
                    emisor=request.user,
                    receptor=vet,
                    estado='pendiente',
                    mensaje=f'Cita aceptada por recepción. Asignada para atención veterinaria.'
                )
        
        # Notificar en tiempo real al grupo de veterinarios
        paciente = getattr(objeto, 'paciente', '-')
        detalle = getattr(objeto, 'motivo', None) or getattr(objeto, 'tipo', '-')
        fecha_str = str(getattr(objeto, 'fecha', '')) if getattr(objeto, 'fecha', None) else ''
        _ws_send('veterinarios', 'notificacion_nueva', {
            'tipo_cita': tipo,
            'objeto_id': cita_id,
            'paciente': str(paciente),
            'detalle': str(detalle)[:60],
            'fecha_cita': fecha_str,
            'message': f'Nueva cita de {tipo} asignada por recepcion',
        })

        messages.success(request, f'{tipo.title()} aceptada y enviada a veterinarios.')
        return redirect('panel_recepcion')
    
    else:
        # --- FLUJO VETERINARIO ---
        # El veterinario confirma que tomará esta cita
        if tipo == 'formulario_contacto':
            objeto.estado = 'Respondido'
        elif tipo == 'mensaje_contacto':
            objeto.estado = 'Leído'
        else:
            objeto.estado = 'Aceptada'
        objeto.save()
        
        # Marcar la notificación del veterinario como aceptada
        notificacion = Notificacion.objects.filter(
            tipo=tipo,
            objeto_id=cita_id,
            receptor=request.user
        ).first()
        if notificacion:
            notificacion.estado = 'aceptada'
            notificacion.save()
        
        # Notificar al panel de recepcion que el vet acepto
        paciente = getattr(objeto, 'paciente', '-')
        _ws_send('recepcion', 'cita_actualizada', {
            'accion': 'aceptada',
            'tipo_cita': tipo,
            'objeto_id': cita_id,
            'paciente': str(paciente),
            'message': f'{tipo.title()} aceptada por el veterinario {request.user.username}',
        })

        messages.success(request, f'{tipo.title()} aceptada. La cita quedará a tu cargo.')
        return redirect('panel_veterinario')

# Rechazar cita - Comportamiento diferente según el rol
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
    elif tipo == 'formulario_contacto':
        objeto = get_object_or_404(FormularioContacto, id=cita_id)
    elif tipo == 'mensaje_contacto':
        objeto = get_object_or_404(MensajeCliente, id=cita_id)
    else:
        messages.error(request, 'Tipo de cita no válido')
        return redirect('panel_recepcion')
    
    # Cambiar estado a Rechazada
    if tipo == 'formulario_contacto':
        objeto.estado = 'Cancelado'
    elif tipo == 'mensaje_contacto':
        # Los mensajes de duda no suelen tener estado 'Rechazado', los dejamos como pendientes o leídos
        # pero para el flujo de notificaciones podemos marcarlos como leídos si se rechazan
        objeto.estado = 'Leído'
    else:
        objeto.estado = 'Rechazada'
    objeto.save()
    
    # Buscar y actualizar la notificación del usuario actual
    notificacion = Notificacion.objects.filter(
        tipo=tipo,
        objeto_id=cita_id,
        receptor=request.user
    ).first()
    
    if notificacion:
        notificacion.estado = 'rechazada'
        notificacion.save()
    
    es_recepcionista = (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista') or request.user.is_staff

    paciente = getattr(objeto, 'paciente', '-')
    if es_recepcionista:
        # Avisar a veterinarios que la cita fue rechazada por recepcion
        _ws_send('veterinarios', 'cita_actualizada', {
            'accion': 'rechazada',
            'tipo_cita': tipo,
            'objeto_id': cita_id,
            'paciente': str(paciente),
            'message': f'{tipo.title()} rechazada por recepcion',
        })
    else:
        # Avisar a recepcion que el vet rechazo la cita
        _ws_send('recepcion', 'cita_actualizada', {
            'accion': 'rechazada',
            'tipo_cita': tipo,
            'objeto_id': cita_id,
            'paciente': str(paciente),
            'message': f'{tipo.title()} rechazada por el veterinario {request.user.username}',
        })

    messages.success(request, f'{tipo.title()} rechazada correctamente')
    return redirect('panel_recepcion' if es_recepcionista else 'panel_veterinario')

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
        objeto = get_object_or_404(Analisis, id=cita_id)
    elif tipo == 'cirugia':
        objeto = get_object_or_404(Cirugia, id=cita_id)
    elif tipo == 'urgencia':
        objeto = get_object_or_404(Urgencia, id=cita_id)
    elif tipo == 'formulario_contacto':
        objeto = get_object_or_404(FormularioContacto, id=cita_id)
    elif tipo == 'mensaje_contacto':
        objeto = get_object_or_404(MensajeCliente, id=cita_id)
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
        if tipo == 'consulta' and Consulta:
            cita = Consulta.objects.create(
                paciente=paciente,
                fecha=fecha,
                motivo=motivo,
                estado='Pendiente'
            )
        elif tipo == 'analisis' and Analisis:
            cita = Analisis.objects.create(
                paciente=paciente,
                fecha=fecha,
                tipo=motivo,  # Para análisis, el motivo es el tipo
                estado='Pendiente'
            )
        elif tipo == 'cirugia' and Cirugia:
            cita = Cirugia.objects.create(
                paciente=paciente,
                fecha=fecha,
                tipo=motivo,  # Para cirugías, el motivo es el tipo
                estado='Pendiente'
            )
        elif tipo == 'urgencia' and Urgencia:
            cita = Urgencia.objects.create(
                paciente=paciente,
                fecha=fecha,
                motivo=motivo,
                estado='Pendiente'
            )
        else:
            messages.error(request, 'Tipo de cita no válido o módulo no disponible')
            return redirect('panel_recepcion')
        
        # Crear notificación para recepcionistas (por rol de perfil)
        recepcionistas = User.objects.filter(perfil__rol='recepcionista')
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
    
    # Notificar a veterinarios (por rol de perfil)
    veterinarios = User.objects.filter(perfil__rol='veterinario')
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
