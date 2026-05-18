# Vistas de usuarios - registro, login y perfiles
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm, PerfilForm
from .forms_servicios import SolicitudConsultaForm, SolicitudAnalisisForm, SolicitudCirugiaForm, SolicitudUrgenciaForm
from .models import Perfil
from consultas.models import Consulta
from laboratorio.models import Analisis
from cirugias.models import Cirugia
from urgencias.models import Urgencia
from mascotas.models import Mascota

# Página de registro
def registro(peticion):
    if peticion.method == 'POST':
        formulario = RegistroForm(peticion.POST)
        if formulario.is_valid():
            try:
                usuario = formulario.save()
                login(peticion, usuario)
                messages.success(peticion, 'El registro se ha completado correctamente.')
                return redirect('home')
            except Exception as e:
                if 'UNIQUE constraint failed: auth_user.username' in str(e):
                    messages.error(peticion, 'Ese nombre de usuario ya está en uso. Por favor, elige otro.')
                elif 'UNIQUE constraint failed: auth_user.email' in str(e):
                    messages.error(peticion, 'Ese correo electrónico ya está registrado. Por favor, usa otro.')
                else:
                    messages.error(peticion, 'Error al registrar el usuario. Por favor, inténtalo de nuevo.')
    else:
        formulario = RegistroForm()
    
    return render(peticion, 'users/registro.html', {'formulario': formulario})

from django.contrib.auth.forms import AuthenticationForm

# Página de login
def login_view(peticion):
    if peticion.method == 'POST':
        formulario = AuthenticationForm(peticion, data=peticion.POST)
        if formulario.is_valid():
            nombre_usuario = formulario.cleaned_data.get('username')
            contraseña = formulario.cleaned_data.get('password')
            usuario = authenticate(username=nombre_usuario, password=contraseña)
            if usuario is not None:
                login(peticion, usuario)
                messages.success(peticion, f'Bienvenido {nombre_usuario}!')
                return redirect('home')
            else:
                messages.error(peticion, 'Usuario o contraseña incorrectos')
    else:
        formulario = AuthenticationForm()
    
    return render(peticion, 'users/login.html', {'formulario': formulario})

# Cerrar sesión
def logout_view(peticion):
    logout(peticion)
    messages.info(peticion, 'Has cerrado sesión correctamente')
    return redirect('home')

# Página del perfil
@login_required
def perfil(peticion):
    # Verificar si se solicita limpiar la autenticación
    if 'clear_auth' in peticion.GET:
        peticion.session.pop('profile_password_verified', None)
        messages.info(peticion, 'Sesión de edición cerrada. Deberás verificar tu identidad nuevamente.')
        return redirect('perfil')
    
    # Verificar si la contraseña ya fue verificada en esta sesión
    password_verified = peticion.session.get('profile_password_verified', False)
    
    if peticion.method == 'POST':
        # Verificar si es el paso de verificación de contraseña
        if 'password_verify' in peticion.POST:
            password = peticion.POST.get('password')
            if peticion.user.check_password(password):
                # Contraseña correcta, guardar en sesión y mostrar formulario de edición
                peticion.session['profile_password_verified'] = True
                formulario = PerfilForm(instance=peticion.user.perfil)
                return render(peticion, 'users/perfil.html', {
                    'formulario': formulario, 
                    'edit_mode': True,
                    'password_verified': True
                })
            else:
                # Contraseña incorrecta
                messages.error(peticion, 'Contraseña incorrecta. Por favor intenta nuevamente.')
                return render(peticion, 'users/perfil.html', {
                    'formulario': PerfilForm(instance=peticion.user.perfil),
                    'edit_mode': False,
                    'password_verified': False
                })
        
        # Es el paso de guardar cambios
        else:
            formulario = PerfilForm(peticion.POST, instance=peticion.user.perfil)
            if formulario.is_valid():
                # Actualizar datos del usuario
                user = peticion.user
                user.first_name = formulario.cleaned_data.get('first_name', '')
                user.last_name = formulario.cleaned_data.get('last_name', '')
                user.email = formulario.cleaned_data.get('email', user.email)
                user.save()
                
                # Actualizar datos del perfil
                perfil = peticion.user.perfil
                perfil.telefono = formulario.cleaned_data.get('telefono', '')
                perfil.direccion = formulario.cleaned_data.get('direccion', '')
                if perfil.rol == 'veterinario':
                    perfil.especialidad = formulario.cleaned_data.get('especialidad', '')
                perfil.save()
                
                messages.success(peticion, 'Tu perfil ha sido actualizado correctamente')
                # Mantener la verificación de contraseña después de guardar
                return redirect('perfil')
            else:
                messages.error(peticion, 'Por favor corrige los errores en el formulario')
                return render(peticion, 'users/perfil.html', {
                    'formulario': formulario,
                    'edit_mode': True,
                    'password_verified': True
                })
    else:
        formulario = PerfilForm(instance=peticion.user.perfil)
    
    # obtener las mascotas del usuario
    mascotas = Mascota.objects.filter(dueno=peticion.user)

    return render(peticion, 'users/perfil.html', {
        'formulario': formulario,
        'edit_mode': password_verified,
        'password_verified': password_verified,
        'mascotas': mascotas
    })

# Lista de agentes (solo admin)
@login_required
def lista_agentes(peticion):
    # Solo admins pueden ver esta página
    if not peticion.user.is_staff:
        messages.error(peticion, 'No tienes permisos para ver esta pagina')
        return redirect('home')
    
    # Obtener todos los agentes (staff)
    agentes = User.objects.filter(is_staff=True).order_by('username')
    
    return render(peticion, 'users/lista_agentes.html', {'agentes': agentes})

# Solicitar consulta
@login_required
def solicitar_consulta(peticion):
    if peticion.method == 'POST':
        formulario = SolicitudConsultaForm(peticion.POST)
        if formulario.is_valid():
            consulta = formulario.save(commit=False)
            consulta.usuario = peticion.user
            consulta.estado = 'Pendiente'
            consulta.save()
            
            # Notificar al recepcionista
            from notificaciones.views import crear_notificacion_automatica
            from django.contrib.auth.models import User
            
            # Buscar recepcionista
            recepcionistas = User.objects.filter(perfil__rol='recepcionista').first()
            if recepcionistas:
                crear_notificacion_automatica(
                    tipo='consulta',
                    objeto_id=consulta.id,
                    emisor=peticion.user,
                    receptor=recepcionistas
                )
            
            messages.success(peticion, 'Tu solicitud de consulta ha sido enviada correctamente')
            return redirect('home')
    else:
        formulario = SolicitudConsultaForm()
    
    return render(peticion, 'users/solicitar_consulta.html', {'formulario': formulario})

# Solicitar análisis
@login_required
def solicitar_analisis(peticion):
    if peticion.method == 'POST':
        formulario = SolicitudAnalisisForm(peticion.POST)
        if formulario.is_valid():
            analisis = formulario.save(commit=False)
            analisis.usuario = peticion.user
            analisis.estado = 'Pendiente'
            analisis.save()
            
            # Notificar al recepcionista
            from notificaciones.views import crear_notificacion_automatica
            from django.contrib.auth.models import User
            
            # Buscar recepcionista
            recepcionistas = User.objects.filter(perfil__rol='recepcionista').first()
            if recepcionistas:
                crear_notificacion_automatica(
                    tipo='analisis',
                    objeto_id=analisis.id,
                    emisor=peticion.user,
                    receptor=recepcionistas
                )
            
            messages.success(peticion, 'Tu solicitud de analisis ha sido enviada correctamente')
            return redirect('home')
    else:
        formulario = SolicitudAnalisisForm()
    
    return render(peticion, 'users/solicitar_analisis.html', {'formulario': formulario})

# Solicitar cirugía
@login_required
def solicitar_cirugia(peticion):
    if peticion.method == 'POST':
        formulario = SolicitudCirugiaForm(peticion.POST)
        if formulario.is_valid():
            cirugia = formulario.save(commit=False)
            cirugia.usuario = peticion.user
            cirugia.estado = 'Pendiente'
            cirugia.save()
            
            # Notificar al recepcionista
            from notificaciones.views import crear_notificacion_automatica
            from django.contrib.auth.models import User
            
            # Buscar recepcionista
            recepcionistas = User.objects.filter(perfil__rol='recepcionista').first()
            if recepcionistas:
                crear_notificacion_automatica(
                    tipo='cirugia',
                    objeto_id=cirugia.id,
                    emisor=peticion.user,
                    receptor=recepcionistas
                )
            
            messages.success(peticion, 'Tu solicitud de cirugía ha sido enviada correctamente')
            return redirect('home')
    else:
        formulario = SolicitudCirugiaForm()
    
    return render(peticion, 'users/solicitar_cirugia.html', {'formulario': formulario})

# Solicitar urgencia
@login_required
def solicitar_urgencia(request):
    if request.method == 'POST':
        form = SolicitudUrgenciaForm(request.POST)
        if form.is_valid():
            urgencia = form.save(commit=False)
            urgencia.usuario = request.user
            urgencia.estado = 'Pendiente'
            urgencia.save()
            
            # Notificar al recepcionista
            from notificaciones.views import crear_notificacion_automatica
            from django.contrib.auth.models import User
            
            # Buscar recepcionista
            recepcionistas = User.objects.filter(perfil__rol='recepcionista').first()
            if recepcionistas:
                crear_notificacion_automatica(
                    tipo='urgencia',
                    objeto_id=urgencia.id,
                    emisor=request.user,
                    receptor=recepcionistas
                )
            
            messages.success(request, 'Tu solicitud de urgencia ha sido enviada correctamente')
            return redirect('home')
    else:
        form = SolicitudUrgenciaForm()
    
    return render(request, 'users/solicitar_urgencia.html', {'form': form})

# Ver mis citas
@login_required
def mis_citas(request):
    # Obtener todas las solicitudes del usuario
    consultas = Consulta.objects.filter(usuario=request.user).order_by('-fecha')
    analisis = Analisis.objects.filter(usuario=request.user).order_by('-fecha')
    cirugias = Cirugia.objects.filter(usuario=request.user).order_by('-fecha')
    urgencias = Urgencia.objects.filter(usuario=request.user).order_by('-fecha')
    
    context = {
        'consultas': consultas,
        'analisis': analisis,
        'cirugias': cirugias,
        'urgencias': urgencias,
    }
    
    return render(request, 'users/mis_citas.html', context)

# Panel de administración

@login_required
@permission_required('users.view_panel_admin', raise_exception=True)
def panel_admin(request):
    # Estadísticas del sistema
    from django.db.models import Count
    from django.utils import timezone
    
    total_clientes = User.objects.filter(perfil__rol='cliente').count()
    total_veterinarios = User.objects.filter(perfil__rol='veterinario').count()
    total_citas_hoy = Consulta.objects.filter(fecha__date=timezone.now().date()).count()
    total_urgencias = Urgencia.objects.filter(estado='Pendiente').count()
    
    # Equipo de trabajo (no clientes)
    equipo = User.objects.filter(perfil__rol__in=['veterinario', 'auxiliar', 'recepcionista', 'admin'])
    
    context = {
        'total_clientes': total_clientes,
        'total_veterinarios': total_veterinarios,
        'total_citas_hoy': total_citas_hoy,
        'total_urgencias': total_urgencias,
        'equipo': equipo,
    }
    
    return render(request, 'users/panel_admin.html', context)

@login_required
@permission_required('auth.view_user', raise_exception=True)
def gestionar_usuarios(request):
    # Obtener todos los usuarios con sus perfiles
    usuarios = User.objects.all().select_related('perfil')
    
    return render(request, 'users/gestionar_usuarios.html', {
        'usuarios': usuarios,
    })

@login_required
@permission_required('auth.add_user', raise_exception=True)
def crear_usuario(request):
    from django.contrib.auth.models import Group
    
    if request.method == 'POST':
        # Crear usuario Django
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        rol = request.POST.get('rol')
        telefono = request.POST.get('telefono')
        
        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Actualizar perfil del usuario
        user.perfil.rol = rol
        user.perfil.telefono = telefono
        user.perfil.save()
        
        # Asignar grupo según rol
        grupo_mapping = {
            'veterinario': 'Veterinarios',
            'auxiliar': 'Auxiliares',
            'recepcionista': 'Recepcionistas',
            'admin': 'Administradores',
        }
        
        if rol in grupo_mapping:
            try:
                grupo = Group.objects.get(name=grupo_mapping[rol])
                user.groups.add(grupo)
                user.is_staff = True
                user.save()
            except Group.DoesNotExist:
                # Si no existe el grupo, dar permisos básicos
                if rol in ['veterinario', 'auxiliar', 'recepcionista', 'admin']:
                    user.is_staff = True
                    user.save()
        
        messages.success(request, f'Usuario {username} creado correctamente con rol de {user.perfil.get_rol_display()}')
        return redirect('gestionar_usuarios')
    
    return render(request, 'users/crear_usuario.html')

@login_required
@permission_required('auth.change_user', raise_exception=True)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.email = request.POST.get('email')
        usuario.is_active = request.POST.get('is_active') == 'on'
        usuario.save()
        
        usuario.perfil.rol = request.POST.get('rol')
        usuario.perfil.telefono = request.POST.get('telefono')
        usuario.perfil.save()
        
        messages.success(request, 'Usuario actualizado correctamente')
        return redirect('gestionar_usuarios')
    
    return render(request, 'users/editar_usuario.html', {'usuario': usuario})

@login_required
@permission_required('auth.delete_user', raise_exception=True)
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    
    # No se puede eliminar al superusuario
    if usuario.is_superuser:
        messages.error(request, 'No puedes eliminar al superusuario')
        return redirect('gestionar_usuarios')
    
    usuario.delete()
    messages.success(request, 'Usuario eliminado correctamente')
    return redirect('gestionar_usuarios')

@login_required
@permission_required('consultas.view_consulta', raise_exception=True)
def gestionar_citas(request):
    # Obtener todas las solicitudes
    consultas = Consulta.objects.all().order_by('-fecha')
    analisis = Analisis.objects.all().order_by('-fecha')
    cirugias = Cirugia.objects.all().order_by('-fecha')
    urgencias = Urgencia.objects.all().order_by('-fecha')
    
    return render(request, 'users/gestionar_citas.html', {
        'consultas': consultas,
        'analisis': analisis,
        'cirugias': cirugias,
        'urgencias': urgencias,
    })

@login_required
@permission_required('users.view_reportes', raise_exception=True)
def reportes(request):
    return render(request, 'users/reportes.html')