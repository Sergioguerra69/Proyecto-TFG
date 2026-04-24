# Vistas del módulo de Laboratorio
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Analisis
from .forms import AnalisisForm
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync  # Temporalmente desactivado

# =============================================
# VISTA PRINCIPAL: Lista todos los análisis
# =============================================
@login_required  # El usuario debe estar logueado para ver esta página
def lista_analisis(request):
    # Mostramos todos los análisis ordenados por fecha (más nuevos primero)
    analisis = Analisis.objects.all().order_by('-fecha')
    return render(request, 'laboratorio/lista_analisis.html', {'analisis': analisis})

# =============================================
# VISTA PARA CREAR: Nuevo análisis de laboratorio
# =============================================
@login_required
def crear_analisis(request):
    # Si el usuario envía el formulario (método POST)
    if request.method == 'POST':
        form = AnalisisForm(request.POST, request.FILES)  # request.FILES para subir PDFs
        if form.is_valid():
            form.save()  # Guardamos el análisis en la base de datos
            
            # Enviar notificación por WebSocket simple
            # try:
            #     channel_layer = get_channel_layer()
            #     async_to_sync(channel_layer.group_send)(
            #         'clinica_notificaciones',
            #         {
            #             'type': 'enviar.notificacion',
            #             'message': 'Nuevo análisis creado',
            #             'tipo': 'analisis'
            #         }
            #     )
            # except:
            #     # Si no funciona, seguimos adelante
            #     pass
            
            messages.success(request, 'Análisis creado correctamente')
            return redirect('lista_analisis')
    else:
        # Si es la primera vez, mostramos el formulario vacío
        form = AnalisisForm()
    
    # Usamos una plantilla genérica para no repetir código
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Nuevo Análisis de Laboratorio',
        'url_cancelar': '/laboratorio/'
    })

# =============================================
# VISTA PARA ACTUALIZAR: Cambiar estado del análisis
# =============================================
@login_required
def actualizar_estado_analisis(request, id):
    # Solo usuarios con permiso de cambiar análisis pueden modificar el estado
    if not request.user.has_perm('laboratorio.change_analisis'):
        messages.error(request, 'No tienes permisos para cambiar estados')
        return redirect('lista_analisis')

    # Si recibimos el formulario con el nuevo estado
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')  # Aquí recibimos el nuevo estado
        
        # Buscamos el análisis y actualizamos el estado
        analisis = get_object_or_404(Analisis, id=id)
        analisis.estado = nuevo_estado
        analisis.save()
        
        # Enviar notificación por WebSocket
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'clinica_notificaciones',
                {
                    'type': 'enviar.notificacion',
                    'message': f'El estado del análisis cambió a: {nuevo_estado}',
                    'tipo': 'analisis'
                }
            )
        except:
            # Si Redis no funciona, la web sigue funcionando
            pass
        
        # Mensaje de éxito para el usuario
        messages.success(request, f'Estado actualizado a: {nuevo_estado}')
        
    return redirect('lista_analisis')

# Editar análisis existente
@login_required
def editar_analisis(request, id):
    analisis = get_object_or_404(Analisis, id=id)
    
    if request.method == 'POST':
        form = AnalisisForm(request.POST, instance=analisis)
        if form.is_valid():
            form.save()
            messages.success(request, 'Análisis actualizado correctamente')
            return redirect('lista_analisis')
    else:
        form = AnalisisForm(instance=analisis)
    
    return render(request, 'form_generico.html', {
        'form': form,
        'titulo': 'Editar Análisis',
        'url_cancelar': '/laboratorio/'
    })

# Eliminar análisis
@login_required
def eliminar_analisis(request, id):
    analisis = get_object_or_404(Analisis, id=id)
    
    if request.method == 'POST':
        analisis.delete()
        messages.success(request, 'Análisis eliminado correctamente')
        return redirect('lista_analisis')
    
    return render(request, 'confirmar_eliminar.html', {
        'objeto': analisis,
        'titulo': 'Eliminar Análisis',
        'url_cancelar': '/laboratorio/'
    })
