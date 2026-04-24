# Vistas para el sistema de notificaciones
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import Notificacion
from consultas.models import Consulta
from laboratorio.models import Analisis
from cirugias.models import Cirugia
from urgencias.models import Urgencia

# Panel de recepción - Vista principal
@login_required
def panel_recepcion(request):
    # Obtener solicitudes pendientes y aceptadas
    consultas = Consulta.objects.filter(estado__in=['Pendiente', 'En Proceso']).order_by('-fecha')
    analisis = Analisis.objects.filter(estado__in=['Pendiente', 'En Proceso']).order_by('-fecha')
    cirugias = Cirugia.objects.filter(estado__in=['Pendiente', 'En Proceso']).order_by('-fecha')
    urgencias = Urgencia.objects.filter(estado__in=['Pendiente', 'En Proceso']).order_by('-fecha')
    
    return render(request, 'notificaciones/panel_recepcion.html', {
        'consultas': consultas,
        'analisis': analisis,
        'cirugias': cirugias,
        'urgencias': urgencias,
    })

# Aceptar solicitud - Cambia estado a 'En Proceso'
@login_required
def aceptar_solicitud(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id)
    
    # Cambiar estado del objeto relacionado
    objeto = notificacion.get_objeto()
    if objeto:
        objeto.estado = 'En Proceso'
        objeto.save()
    
    # Actualizar notificación
    notificacion.estado = 'aceptada'
    notificacion.save()
    
    # Notificar a veterinarios de forma simple
    veterinarios = User.objects.filter(groups__name='veterinarios')
    for vet in veterinarios:
        Notificacion.objects.create(
            tipo=notificacion.tipo,
            objeto_id=notificacion.objeto_id,
            emisor=request.user,
            receptor=vet,
            estado='pendiente'
        )
    
    messages.success(request, 'Solicitud aceptada correctamente')
    return redirect('panel_recepcion')

# Rechazar solicitud - Cambia estado a 'Cancelada'
@login_required
def rechazar_solicitud(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id)
    
    # Cambiar estado del objeto relacionado
    objeto = notificacion.get_objeto()
    if objeto:
        objeto.estado = 'Cancelada'
        objeto.save()
    
    # Actualizar notificación
    notificacion.estado = 'rechazada'
    notificacion.save()
    
    messages.success(request, 'Solicitud rechazada correctamente')
    return redirect('panel_recepcion')

# Panel de veterinarios - Vista simple para veterinarios
@login_required
def panel_veterinario(request):
    # Obtener notificaciones pendientes para este veterinario
    notificaciones = Notificacion.objects.filter(
        receptor=request.user,
        estado='pendiente'
    ).order_by('-fecha_creacion')
    
    return render(request, 'notificaciones/panel_veterinario.html', {
        'notificaciones': notificaciones,
    })

# Mis Notificaciones - Vista para ver todas las notificaciones del veterinario
@login_required
def mis_notificaciones(request):
    # Obtener todas las notificaciones para este veterinario
    notificaciones = Notificacion.objects.filter(
        receptor=request.user
    ).order_by('-fecha_creacion')
    
    return render(request, 'notificaciones/mis_notificaciones.html', {
        'notificaciones': notificaciones,
    })



# Aceptar cita - Cambia estado a 'En Proceso'
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
    
    # Cambiar estado
    objeto.estado = 'En Proceso'
    objeto.save()
    
    # Notificar a veterinarios
    veterinarios = User.objects.filter(groups__name='veterinarios')
    for vet in veterinarios:
        Notificacion.objects.create(
            tipo=tipo,
            objeto_id=cita_id,
            emisor=request.user,
            receptor=vet,
            estado='pendiente'
        )
    
    messages.success(request, f'{tipo.title()} aceptada correctamente')
    return redirect('panel_recepcion')

# Rechazar cita - Cambia estado a 'Cancelada'
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
    
    # Cambiar estado
    objeto.estado = 'Cancelada'
    objeto.save()
    
    messages.success(request, f'{tipo.title()} rechazada correctamente')
    return redirect('panel_recepcion')

# Eliminar cita - Elimina el objeto completamente
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

# Crear nueva cita
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
        recepcionistas = User.objects.filter(groups__name='recepcionistas')
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

# Configurar permisos de usuarios - Vista para administradores
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

# Crear notificación automática
def crear_notificacion_automatica(tipo, objeto_id, emisor, receptor):
    """Crea notificaciones automáticamente cuando un cliente solicita un servicio"""
    Notificacion.objects.create(
        tipo=tipo,
        objeto_id=objeto_id,
        emisor=emisor,
        receptor=receptor,
        estado='pendiente'
    )
