# Vistas: funciones que reciben la peticion del usuario y devuelven la pagina HTML
# Este archivo sirve para gestionar el envío del formulario de contacto
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConsultaForm

def contacto(request):
    # Si el usuario pulsa el botón de enviar (POST)
    if request.method == 'POST':
        formulario = ConsultaForm(request.POST)
        if formulario.is_valid():
            # Guardamos los datos en la base de datos
            formulario.save()
            # Mandamos un mensaje de éxito que saldrá en el HTML
            messages.success(request, 'El mensaje ha sido recibido correctamente. Se le responderá a la brevedad.')
            return redirect('contacto')
    else:
        # Si solo entra a ver la página, le damos el formulario vacío
        formulario = ConsultaForm()
    
    return render(request, 'contacto/contacto.html', {'form': formulario})
