# Vistas del módulo de Urgencias
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Urgencia
from .forms import UrgenciaForm
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync  # Temporalmente desactivado

# =============================================
# VISTA PRINCIPAL: Lista todas las urgencias
# =============================================
@login_required  # El usuario debe estar logueado
def lista_urgencias(request):
    # Mostramos todas las urgencias ordenadas por fecha (más recientes primero)
    urgencias = Urgencia.objects.all().order_by('-fecha')
    return render(request, 'urgencias/lista_urgencias.html', {'urgencias': urgencias})

# =============================================
# VISTA PARA CREAR: Nueva urgencia veterinaria
# =============================================
@login_required
def crear_urgencia(request):
    # Si el usuario envía el formulario de urgencia
    if request.method == 'POST':
        form = UrgenciaForm(request.POST)
        if form.is_valid():
            form.save()  # Guardamos la urgencia en la base de datos
            
            # Enviamos notificación por WebSocket (es urgencia, debe ser rápido)
            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'clinica_notificaciones',
                    {
                        'type': 'enviar.notificacion',
                        'message': '¡NUEVA URGENCIA REGISTRADA!'
                    }
                )
            except:
                # Si Redis no funciona, la web sigue funcionando
                pass
            
            # Mensaje de éxito para el usuario
            messages.success(request, 'Urgencia registrada correctamente')
            return redirect('lista_urgencias')
    else:
        # Mostramos el formulario vacío
        form = UrgenciaForm()
    
    # Usamos plantilla genérica
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Registrar Urgencia Veterinaria',
        'url_cancelar': '/urgencias/'
    })

# =============================================
# VISTA PARA ACTUALIZAR: Cambiar estado de urgencia
# =============================================
@login_required
def actualizar_estado_urgencia(request, id):
    # Solo usuarios con permiso de cambiar urgencias pueden modificar el estado
    if not request.user.has_perm('urgencias.change_urgencia'):
        messages.error(request, 'No tienes permisos para cambiar estados')
        return redirect('lista_urgencias')

    # Si recibimos el formulario con el nuevo estado
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        
        # Buscamos la urgencia y actualizamos el estado
        urgencia = get_object_or_404(Urgencia, id=id)
        urgencia.estado = nuevo_estado
        urgencia.save()
        
        # Enviar notificación por WebSocket simple
        # try:
        #     channel_layer = get_channel_layer()
        #     async_to_sync(channel_layer.group_send)(
        #         'clinica_notificaciones',
        #         {
        #             'type': 'enviar.notificacion',
        #             'message': f'Estado urgencia: {nuevo_estado}',
        #             'tipo': 'urgencia'
        #         }
        #     )
        # except:
        #     # Si no funciona, seguimos adelante
        #     pass
        
        # Mensaje de éxito para el usuario
        messages.success(request, f'Estado actualizado a: {nuevo_estado}')
        
    return redirect('lista_urgencias')

# Editar urgencia existente
@login_required
@permission_required('urgencias.change_urgencia', raise_exception=True)
def editar_urgencia(request, id):
    urgencia = get_object_or_404(Urgencia, id=id)
    
    if request.method == 'POST':
        form = UrgenciaForm(request.POST, instance=urgencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Urgencia actualizada correctamente')
            return redirect('lista_urgencias')
    else:
        form = UrgenciaForm(instance=urgencia)
    
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Editar Urgencia',
        'url_cancelar': '/urgencias/'
    })

# Eliminar urgencia
@login_required
@permission_required('urgencias.delete_urgencia', raise_exception=True)
def eliminar_urgencia(request, id):
    urgencia = get_object_or_404(Urgencia, id=id)
    
    if request.method == 'POST':
        urgencia.delete()
        messages.success(request, 'Urgencia eliminada correctamente')
        return redirect('lista_urgencias')
    
    return render(request, 'confirmar_eliminar.html', {
        'objeto': urgencia,
        'titulo': 'Eliminar Urgencia',
        'url_cancelar': '/urgencias/'
    })
