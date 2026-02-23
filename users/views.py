from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, PerfilForm
from .models import Perfil

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro completado! Bienvenido')
            return redirect('home')
    else:
        form = RegistroForm()
    
    return render(request, 'users/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, '¡Has iniciado sesión!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada')
    return redirect('home')

@login_required
def perfil(request):
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    
    return render(request, 'users/perfil.html', {
        'form': form,
        'perfil': perfil
    })