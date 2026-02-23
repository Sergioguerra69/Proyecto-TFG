# Vistas: funciones que reciben la peticion del usuario y devuelven la pagina HTML
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, PerfilForm
from .models import Perfil

# Vista de registro
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'El registro se ha completado correctamente.')
            return redirect('home')
    else:
        form = RegistroForm()
    
    return render(request, 'users/registro.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm

# Vista de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Sesión iniciada correctamente.')
                return redirect('home')
        else:
            messages.error(request, 'Los datos de acceso son incorrectos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

# Vista de logout
def logout_view(request):
    logout(request)
    messages.info(request, 'La sesión se ha cerrado correctamente.')
    return redirect('home')

# Vista del perfil (solo para usuarios logueados)
@login_required
def perfil(request):
    # Obtengo el perfil del usuario
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'La información del perfil ha sido actualizada.')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    
    return render(request, 'users/perfil.html', {
        'form': form,
        'perfil': perfil
    })