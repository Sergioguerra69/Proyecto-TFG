# Vistas del módulo de Urgencias
# Aquí gestionamos las urgencias veterinarias 24h

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Urgencia
from .forms import UrgenciaForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    # Solo el personal puede cambiar los estados de urgencias
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para cambiar estados')
        return redirect('lista_urgencias')

    # Si recibimos el formulario con el nuevo estado
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')  # Recibimos el nuevo estado
        
        # Usamos get_object_or_404 para evitar errores 500 si el ID no existe
        urgencia = get_object_or_404(Urgencia, id=id)     # Buscamos la urgencia
        urgencia.estado = nuevo_estado                      # Cambiamos el estado
        urgencia.save()                                     # Guardamos en la BD

        # Enviamos notificación por WebSocket (es urgencia, es importante)
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'clinica_notificaciones',
                {
                    'type': 'enviar.notificacion',
                    'message': f'El estado de la urgencia cambió a: {nuevo_estado}'
                }
            )
        except:
            # Si Redis no funciona, la web sigue funcionando
            pass
        
        # Mensaje de éxito para el usuario
        messages.success(request, f'Estado actualizado a: {nuevo_estado}')
        
    return redirect('lista_urgencias')
