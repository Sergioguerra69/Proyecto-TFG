# Vistas para el sistema de contacto
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from .models import FormularioContacto, RespuestaContacto, MensajeCliente, RespuestaMensaje, AsignacionSolicitud, NotificacionVeterinario
from .forms import FormularioContactoForm, RespuestaContactoForm, MensajeClienteForm, RespuestaMensajeForm, AsignacionSolicitudForm

# Vista para el formulario de contacto público
def contacto_publico(request):
    # Determinar qué tipo de formulario se está enviando
    form_contacto = FormularioContactoForm()
    form_mensaje = MensajeClienteForm()
    
    if request.method == 'POST':
        # Verificar si es un formulario de contacto o un mensaje de duda
        if 'tipo_formulario' in request.POST:
            if request.POST['tipo_formulario'] == 'contacto':
                form_contacto = FormularioContactoForm(request.POST)
                if form_contacto.is_valid():
                    formulario = form_contacto.save()
                    
                    # Crear notificación para los recepcionistas
                    from notificaciones.models import Notificacion
                    recepcionistas = User.objects.filter(perfil__rol='recepcionista')
                    for recep in recepcionistas:
                        admin_user = User.objects.filter(username='admin').first()
                        emisor = request.user if request.user.is_authenticated else admin_user
                        Notificacion.objects.create(
                            tipo='formulario_contacto',
                            objeto_id=formulario.id,
                            emisor=emisor,
                            receptor=recep,
                            estado='pendiente',
                            mensaje=f"Nuevo formulario de contacto de {formulario.nombre}"
                        )
                    
                    messages.success(request, 'Tu formulario de contacto ha sido enviado correctamente. Nos pondremos en contacto contigo pronto.')
                    return redirect('contacto_publico')
            elif request.POST['tipo_formulario'] == 'mensaje':
                form_mensaje = MensajeClienteForm(request.POST)
                if form_mensaje.is_valid():
                    mensaje_obj = form_mensaje.save()
                    
                    # Crear notificación para los recepcionistas
                    from notificaciones.models import Notificacion
                    recepcionistas = User.objects.filter(perfil__rol='recepcionista')
                    for recep in recepcionistas:
                        admin_user = User.objects.filter(username='admin').first()
                        emisor = request.user if request.user.is_authenticated else admin_user
                        Notificacion.objects.create(
                            tipo='mensaje_contacto',
                            objeto_id=mensaje_obj.id,
                            emisor=emisor,
                            receptor=recep,
                            estado='pendiente',
                            mensaje=f"Nuevo mensaje de duda de {mensaje_obj.nombre}"
                        )
                    
                    messages.success(request, 'Tu duda ha sido enviada correctamente. Nuestro equipo te responderá pronto.')
                    return redirect('contacto_publico')
    
    return render(request, 'contacto/contacto.html', {
        'form': form_contacto,
        'form_mensaje': form_mensaje,
        'titulo': 'Contacto'
    })

# Vista para el panel de recepcionista - gestionar formularios de contacto y mensajes
@login_required
def panel_contactos_recepcionista(request):
    # Verificar si es recepcionista
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    # Obtener formularios de contacto pendientes
    formularios_pendientes = FormularioContacto.objects.filter(estado='Pendiente')
    
    # Obtener formularios de contacto respondidos
    formularios_respondidos = FormularioContacto.objects.filter(estado='Respondido')
    
    # Obtener mensajes de clientes pendientes
    mensajes_pendientes = MensajeCliente.objects.filter(estado='Pendiente')
    
    # Obtener mensajes de clientes respondidos
    mensajes_respondidos = MensajeCliente.objects.filter(estado='Respondido')
    
    return render(request, 'contacto/panel_recepcionista.html', {
        'formularios_pendientes': formularios_pendientes,
        'formularios_respondidos': formularios_respondidos,
        'mensajes_pendientes': mensajes_pendientes,
        'mensajes_respondidos': mensajes_respondidos,
        'titulo': 'Panel de Contactos - Recepción'
    })

# Vista para gestionar mensajes de clientes
@login_required
def panel_mensajes_recepcionista(request):
    # Verificar si es recepcionista
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    # Obtener mensajes pendientes
    mensajes_pendientes = MensajeCliente.objects.filter(estado='Pendiente')
    
    # Obtener mensajes leídos/respondidos
    mensajes_procesados = MensajeCliente.objects.filter(estado__in=['Leído', 'Respondido', 'Cerrado'])
    
    return render(request, 'contacto/panel_mensajes.html', {
        'mensajes_pendientes': mensajes_pendientes,
        'mensajes_procesados': mensajes_procesados,
        'titulo': 'Panel de Mensajes - Recepción'
    })

# Vista para ver y responder un mensaje de cliente
@login_required
def ver_mensaje_cliente(request, mensaje_id):
    # Verificar si es recepcionista
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    mensaje = get_object_or_404(MensajeCliente, id=mensaje_id)
    
    # Marcar como leído si está pendiente
    if mensaje.estado == 'Pendiente':
        mensaje.estado = 'Leído'
        mensaje.save()
    
    # Obtener respuestas anteriores
    respuestas = RespuestaMensaje.objects.filter(mensaje=mensaje).order_by('fecha_creacion')
    
    # Formulario para responder
    if request.method == 'POST':
        form_respuesta = RespuestaMensajeForm(request.POST)
        if form_respuesta.is_valid():
            respuesta = form_respuesta.save(commit=False)
            respuesta.mensaje = mensaje
            respuesta.autor = request.user
            respuesta.es_cliente = False  # Es respuesta del recepcionista
            respuesta.save()
            
            # Actualizar estado del mensaje
            mensaje.estado = 'Respondido'
            mensaje.respondido_por = request.user
            mensaje.fecha_respuesta = timezone.now()
            mensaje.save()
            
            messages.success(request, 'Respuesta enviada correctamente.')
            return redirect('ver_mensaje_cliente', mensaje_id=mensaje_id)
    else:
        form_respuesta = RespuestaMensajeForm()
    
    return render(request, 'contacto/ver_mensaje_cliente.html', {
        'mensaje': mensaje,
        'respuestas': respuestas,
        'form_respuesta': form_respuesta,
        'titulo': f'Mensaje de {mensaje.nombre}'
    })

# Vista para marcar mensaje como leído
@login_required
def marcar_mensaje_leido(request, mensaje_id):
    # Verificar si es recepcionista
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista'):
        return JsonResponse({'success': False, 'error': 'No tienes permisos'})
    
    if request.method == 'POST':
        mensaje = get_object_or_404(MensajeCliente, id=mensaje_id)
        if mensaje.estado == 'Pendiente':
            mensaje.estado = 'Leído'
            mensaje.save()
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

# Vista para cerrar mensaje
@login_required
def cerrar_mensaje(request, mensaje_id):
    # Verificar si es recepcionista
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista'):
        return JsonResponse({'success': False, 'error': 'No tienes permisos'})
    
    if request.method == 'POST':
        mensaje = get_object_or_404(MensajeCliente, id=mensaje_id)
        mensaje.estado = 'Cerrado'
        mensaje.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

# Vista para responder un formulario de contacto
@login_required
def responder_formulario(request, formulario_id):
    # Verificar si es recepcionista
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    formulario = get_object_or_404(FormularioContacto, id=formulario_id)
    
    if request.method == 'POST':
        respuesta_form = RespuestaContactoForm(request.POST)
        if respuesta_form.is_valid():
            # Crear la respuesta
            respuesta = RespuestaContacto.objects.create(
                formulario=formulario,
                autor=request.user,
                contenido=respuesta_form.cleaned_data['contenido']
            )
            
            # Actualizar el formulario original
            formulario.estado = 'Respondido'
            formulario.respondido_por = request.user
            formulario.fecha_respuesta = timezone.now()
            formulario.save()
            
            messages.success(request, 'Respuesta enviada correctamente.')
            return redirect('panel_contactos_recepcionista')
    else:
        respuesta_form = RespuestaContactoForm()
    
    return render(request, 'contacto/responder_formulario.html', {
        'formulario': formulario,
        'respuesta_form': respuesta_form,
        'titulo': f'Responder a {formulario.nombre}'
    })

# Vista para el panel personal del cliente - ver sus mensajes y respuestas
@login_required
def panel_contactos_cliente(request):
    # Obtener formularios enviados por este usuario (basado en email)
    formularios_enviados = FormularioContacto.objects.filter(email=request.user.email)
    
    # Obtener respuestas a esos formularios
    for formulario in formularios_enviados:
        formulario.respuestas = formulario.respuestas.all()
    
    return render(request, 'contacto/panel_cliente.html', {
        'formularios_enviados': formularios_enviados,
        'titulo': 'Mis Mensajes de Contacto'
    })

# Vista para que el cliente pueda responder a una respuesta
@login_required
def responder_respuesta(request, formulario_id):
    formulario = get_object_or_404(FormularioContacto, id=formulario_id, email=request.user.email)
    
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            # Crear nueva respuesta del cliente
            RespuestaContacto.objects.create(
                formulario=formulario,
                autor=request.user,
                contenido=f"[CLIENTE RESPONDE]: {contenido}"
            )
            
            messages.success(request, 'Tu respuesta ha sido enviada.')
            return redirect('panel_contactos_cliente')
    
    return render(request, 'contacto/responder_respuesta.html', {
        'formulario': formulario,
        'titulo': f'Responder a tu mensaje sobre "{formulario.asunto}"'
    })

# Vista para ver detalles de un formulario
@login_required
def ver_formulario(request, formulario_id):
    formulario = get_object_or_404(FormularioContacto, id=formulario_id)
    
    # Verificar permisos: recepcionista o el propio cliente
    es_recepcionista = hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista'
    es_propietario = formulario.email == request.user.email
    
    if not (es_recepcionista or es_propietario):
        messages.error(request, 'No tienes permisos para ver este formulario.')
        return redirect('home')
    
    # Obtener todas las respuestas
    respuestas = formulario.respuestas.all()
    
    return render(request, 'contacto/ver_formulario.html', {
        'formulario': formulario,
        'respuestas': respuestas,
        'es_recepcionista': es_recepcionista,
        'titulo': f'Detalles del formulario'
    })

# Vista para asignar solicitud a veterinario
@login_required
def asignar_solicitud(request, formulario_id):
    # Verificar si es recepcionista
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'recepcionista'):
        messages.error(request, 'No tienes permisos para asignar solicitudes.')
        return redirect('home')
    
    formulario = get_object_or_404(FormularioContacto, id=formulario_id)
    
    if request.method == 'POST':
        form_asignacion = AsignacionSolicitudForm(request.POST)
        if form_asignacion.is_valid():
            asignacion = form_asignacion.save(commit=False)
            asignacion.formulario = formulario
            asignacion.asignado_por = request.user
            asignacion.save()
            
            # Actualizar estado del formulario
            formulario.estado = 'Respondido'
            formulario.respondido_por = request.user
            formulario.fecha_respuesta = timezone.now()
            formulario.save()
            
            # Crear notificación para el veterinario usando el sistema existente
            from notificaciones.models import Notificacion
            Notificacion.objects.create(
                tipo='formulario_contacto',
                objeto_id=formulario.id,
                emisor=request.user,
                receptor=asignacion.veterinario,
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
                        'message': f'Nueva solicitud de contacto de {formulario.nombre} {formulario.apellidos} asignada'
                    }
                )
            except:
                pass
            
            messages.success(request, f'Solicitud asignada correctamente a {asignacion.veterinario.username}.')
            return redirect('panel_contactos_recepcionista')
    else:
        form_asignacion = AsignacionSolicitudForm()
    
    return render(request, 'contacto/asignar_solicitud.html', {
        'formulario': formulario,
        'form_asignacion': form_asignacion,
        'titulo': f'Asignar solicitud de {formulario.nombre}'
    })

# Vista para el panel de veterinarios
@login_required
def panel_veterinario(request):
    # Verificar si es veterinario
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'veterinario'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    # Obtener solicitudes asignadas al veterinario
    asignaciones_pendientes = AsignacionSolicitud.objects.filter(
        veterinario=request.user, 
        estado='Asignada'
    )
    
    asignaciones_aceptadas = AsignacionSolicitud.objects.filter(
        veterinario=request.user, 
        estado='Aceptada'
    )
    
    asignaciones_completadas = AsignacionSolicitud.objects.filter(
        veterinario=request.user, 
        estado='Completada'
    )
    
    # Obtener notificaciones no leídas
    notificaciones_no_leidas = NotificacionVeterinario.objects.filter(
        veterinario=request.user, 
        leida=False
    )
    
    return render(request, 'contacto/panel_veterinario.html', {
        'asignaciones_pendientes': asignaciones_pendientes,
        'asignaciones_aceptadas': asignaciones_aceptadas,
        'asignaciones_completadas': asignaciones_completadas,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'titulo': 'Panel Veterinario'
    })

# Vista para ver detalles de formulario de contacto
@login_required
def ver_formulario_contacto(request, formulario_id):
    formulario = get_object_or_404(FormularioContacto, id=formulario_id)
    
    # Verificar permisos (veterinarios o recepcionistas pueden ver)
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol in ['veterinario', 'recepcionista']):
        messages.error(request, 'No tienes permisos para ver este formulario.')
        return redirect('home')
    
    return render(request, 'contacto/ver_formulario_contacto.html', {
        'formulario': formulario,
        'titulo': f'Formulario de {formulario.nombre}'
    })

# Vista para ver detalles de solicitud asignada
@login_required
def ver_solicitud_asignada(request, asignacion_id):
    asignacion = get_object_or_404(AsignacionSolicitud, id=asignacion_id)
    
    # Verificar permisos
    es_veterinario = hasattr(request.user, 'perfil') and request.user.perfil.rol == 'veterinario'
    if not (es_veterinario and 
            asignacion.veterinario == request.user):
        messages.error(request, 'No tienes permisos para ver esta solicitud.')
        return redirect('home')
    
    # Marcar notificaciones relacionadas como leídas
    NotificacionVeterinario.objects.filter(
        veterinario=request.user,
        asignacion=asignacion,
        leida=False
    ).update(leida=True, fecha_lectura=timezone.now())
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'aceptar':
            asignacion.estado = 'Aceptada'
            asignacion.fecha_aceptacion = timezone.now()
            asignacion.save()
            
            # Notificar al recepcionista
            NotificacionVeterinario.objects.create(
                veterinario=asignacion.asignado_por,
                tipo='aceptacion',
                titulo=f'Solicitud aceptada: {asignacion.formulario.asunto}',
                mensaje=f'{request.user.username} ha aceptado la solicitud de {asignacion.formulario.nombre}.'
            )
            
            messages.success(request, 'Solicitud aceptada correctamente.')
            
        elif accion == 'rechazar':
            asignacion.estado = 'Rechazada'
            asignacion.save()
            
            # Notificar al recepcionista
            NotificacionVeterinario.objects.create(
                veterinario=asignacion.asignado_por,
                tipo='rechazo',
                titulo=f'Solicitud rechazada: {asignacion.formulario.asunto}',
                mensaje=f'{request.user.username} ha rechazado la solicitud de {asignacion.formulario.nombre}.'
            )
            
            messages.success(request, 'Solicitud rechazada.')
            
        elif accion == 'completar':
            asignacion.estado = 'Completada'
            asignacion.fecha_completacion = timezone.now()
            asignacion.save()
            
            messages.success(request, 'Solicitud completada.')
            
        return redirect('panel_contactos_veterinario')
    
    return render(request, 'contacto/ver_solicitud_asignada.html', {
        'asignacion': asignacion,
        'titulo': f'Solicitud de {asignacion.formulario.nombre}'
    })

# Vista para ver notificaciones del veterinario
@login_required
def ver_notificaciones_veterinario(request):
    # Verificar si es veterinario
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'veterinario'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    notificaciones = NotificacionVeterinario.objects.filter(
        veterinario=request.user
    ).order_by('-fecha_creacion')
    
    return render(request, 'contacto/notificaciones_veterinario.html', {
        'notificaciones': notificaciones,
        'titulo': 'Notificaciones'
    })

# Vista para que el veterinario gestione una solicitud asignada
@login_required
def gestionar_solicitud_veterinario(request, notificacion_id):
    # Verificar si es veterinario
    if not (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'veterinario'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    # Obtener la notificación
    from notificaciones.models import Notificacion
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, receptor=request.user)
    
    # Verificar que sea una notificación de formulario de contacto
    if notificacion.tipo != 'formulario_contacto':
        messages.error(request, 'Tipo de notificación no válido.')
        return redirect('panel_veterinario')
    
    # Obtener el formulario de contacto
    formulario = get_object_or_404(FormularioContacto, id=notificacion.objeto_id)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'aceptar':
            # Cambiar estado de la notificación
            notificacion.estado = 'aceptada'
            notificacion.fecha_lectura = timezone.now()
            notificacion.save()
            
            # Opcional: Crear asignación si no existe
            asignacion, created = AsignacionSolicitud.objects.get_or_create(
                formulario=formulario,
                veterinario=request.user,
                defaults={
                    'asignado_por': User.objects.filter(perfil__rol='recepcionista').first(),
                    'estado': 'Aceptada',
                    'fecha_aceptacion': timezone.now()
                }
            )
            
            messages.success(request, 'Solicitud aceptada correctamente.')
            
        elif accion == 'rechazar':
            # Cambiar estado de la notificación
            notificacion.estado = 'rechazada'
            notificacion.fecha_lectura = timezone.now()
            notificacion.save()
            
            messages.success(request, 'Solicitud rechazada.')
            
        return redirect('panel_contactos_veterinario')
    
    return render(request, 'contacto/gestionar_solicitud_veterinario.html', {
        'formulario': formulario,
        'notificacion': notificacion,
        'titulo': f'Gestionar solicitud de {formulario.nombre} {formulario.apellidos}'
    })
