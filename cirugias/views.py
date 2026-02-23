# Vistas del módulo de Cirugías
# Aquí gestionamos las cirugías (solo personal autorizado)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Cirugia
from .forms import CirugiaForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Función para verificar si el usuario es administrativo (staff)
def es_administrativo(user):
    return user.is_staff

# =============================================
# VISTA PRINCIPAL: Lista todas las cirugías (solo staff)
# =============================================
@login_required  # Debe estar logueado
@user_passes_test(es_administrativo)  # Y debe ser personal autorizado
def lista_cirugias(request):
    # Mostramos todas las cirugías ordenadas por fecha
    cirugias = Cirugia.objects.all().order_by('-fecha')
    return render(request, 'cirugias/lista_cirugias.html', {'cirugias': cirugias})

# =============================================
# VISTA PARA CREAR: Nueva cirugía (solo staff)
# =============================================
@login_required
@user_passes_test(es_administrativo)
def crear_cirugia(request):
    # Si el usuario envía el formulario
    if request.method == 'POST':
        form = CirugiaForm(request.POST)
        if form.is_valid():
            form.save()  # Guardamos la cirugía en la base de datos
            
            # Enviamos notificación por WebSocket
            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'clinica_notificaciones',
                    {
                        'type': 'enviar.notificacion',
                        'message': '¡Nueva cirugía programada!'
                    }
                )
            except:
                # Si Redis no funciona, la web sigue funcionando
                pass
            
            # Mensaje de éxito para el usuario
            messages.success(request, 'Cirugía programada correctamente')
            return redirect('lista_cirugias')
    else:
        # Mostramos el formulario vacío
        form = CirugiaForm()
    
    # Usamos plantilla genérica
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Programar Nueva Cirugía',
        'url_cancelar': '/cirugias/'
    })

# =============================================
# VISTA PARA ACTUALIZAR: Cambiar estado de cirugía
# =============================================
@login_required
def actualizar_estado_cirugia(request, id):
    # Solo el personal puede cambiar los estados de cirugías
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para cambiar estados')
        return redirect('lista_cirugias')

    # Si recibimos el formulario con el nuevo estado
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')  # Recibimos el nuevo estado
        
        # Usamos get_object_or_404 para evitar errores 500 si el ID no existe
        cirugia = get_object_or_404(Cirugia, id=id)        # Buscamos la cirugía
        cirugia.estado = nuevo_estado                        # Cambiamos el estado
        cirugia.save()                                       # Guardamos en la BD

        # Enviamos notificación por WebSocket
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'clinica_notificaciones',
                {
                    'type': 'enviar.notificacion',
                    'message': f'El estado de la cirugía cambió a: {nuevo_estado}'
                }
            )
        except:
            # Si Redis no funciona, la web sigue funcionando
            pass
        
        # Mensaje de éxito para el usuario
        messages.success(request, f'Estado actualizado a: {nuevo_estado}')
        
    return redirect('lista_cirugias')
