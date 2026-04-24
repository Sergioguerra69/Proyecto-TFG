# Vistas del módulo de Estética
# Aquí gestionamos los servicios de peluquería y estética

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServicioEstetica
from .forms import EsteticaForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# =============================================
# VISTA PRINCIPAL: Lista todos los servicios de estética
# =============================================
@login_required  # El usuario debe estar logueado
def lista_estetica(request):
    # Mostramos todos los servicios de estética ordenados por fecha
    servicios = ServicioEstetica.objects.all().order_by('-fecha')
    return render(request, 'estetica/lista_estetica.html', {'servicios': servicios})

# =============================================
# VISTA PARA CREAR: Nuevo servicio de estética
# =============================================
@login_required
def crear_estetica(request):
    # Si el usuario envía el formulario
    if request.method == 'POST':
        form = EsteticaForm(request.POST)
        if form.is_valid():
            form.save()  # Guardamos el servicio de estética
            
            # Enviamos notificación por WebSocket
            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'clinica_notificaciones',
                    {
                        'type': 'enviar.notificacion',
                        'message': '¡Nuevo servicio de estética creado!'
                    }
                )
            except:
                # Si Redis no funciona, la web sigue funcionando
                pass
            
            # Mensaje de éxito para el usuario
            messages.success(request, 'Servicio de estética creado correctamente')
            return redirect('lista_estetica')
    else:
        # Mostramos el formulario vacío
        form = EsteticaForm()
    
    # Usamos plantilla genérica
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Nuevo Servicio de Estética',
        'url_cancelar': '/estetica/'
    })

# =============================================
# VISTA PARA ACTUALIZAR: Cambiar estado del servicio
# =============================================
@login_required
def actualizar_estado_estetica(request, id):
    # Solo el personal puede cambiar los estados
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para cambiar estados')
        return redirect('lista_estetica')

    # Si recibimos el formulario con el nuevo estado
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')  # Recibimos el nuevo estado
        
        # Usamos get_object_or_404 para evitar errores 500 si el ID no existe
        servicio = get_object_or_404(ServicioEstetica, id=id)  # Buscamos el servicio
        servicio.estado = nuevo_estado                          # Cambiamos el estado
        servicio.save()                                         # Guardamos en la BD

        # Enviamos notificación por WebSocket
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'clinica_notificaciones',
                {
                    'type': 'enviar.notificacion',
                    'message': f'El estado del servicio de estética cambió a: {nuevo_estado}'
                }
            )
        except:
            # Si Redis no funciona, la web sigue funcionando
            pass
        
        # Mensaje de éxito para el usuario
        messages.success(request, f'Estado actualizado a: {nuevo_estado}')
        
    return redirect('lista_estetica')
