# Vistas del módulo de Consultas
# Aquí gestionamos las consultas médicas

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Consulta
from .forms import ConsultaForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# =============================================
# VISTA PRINCIPAL: Lista todas las consultas
# =============================================
@login_required  # El usuario debe estar logueado
def lista_consultas(request):
    # Mostramos todas las consultas ordenadas por fecha
    consultas = Consulta.objects.all().order_by('-fecha')
    return render(request, 'consultas/lista_consultas.html', {'consultas': consultas})

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
    # Solo el personal puede cambiar los estados
    if not request.user.is_staff:
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
