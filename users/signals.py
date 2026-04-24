# Signals: funciones que se ejecutan solas cuando pasa algo
# Aquí damos permisos según el tipo de usuario

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from .models import Perfil
from consultas.models import Consulta
from laboratorio.models import Analisis
from cirugias.models import Cirugia
from urgencias.models import Urgencia


# Cuando se guarda un perfil, esta funcion se ejecuta sola
@receiver(post_save, sender=Perfil)
def asignar_permisos_según_rol(sender, instance, created, **kwargs):
    usuario = instance.usuario
    rol = instance.rol
    
    # Borramos los permisos que tenia antes
    usuario.user_permissions.clear()
    
    # Aqui definimos que puede hacer cada tipo de usuario
    permisos_por_rol = {
        'admin': {
            'is_staff': True,
            'is_superuser': True,
            'permisos': [
                # El admin puede hacer TODO
                'add_consulta', 'view_consulta', 'change_consulta', 'delete_consulta',
                'add_analisis', 'view_analisis', 'change_analisis', 'delete_analisis',
                'add_cirugia', 'view_cirugia', 'change_cirugia', 'delete_cirugia',
                'add_urgencia', 'view_urgencia', 'change_urgencia', 'delete_urgencia',
                # Permisos para notificaciones
                'view_notificacion', 'change_notificacion', 'delete_notificacion',
                # Admin también gestiona usuarios
                'add_user', 'view_user', 'change_user', 'delete_user',
            ]
        },
        'veterinario': {
            'is_staff': True,
            'is_superuser': False,
            'permisos': [
                # El veterinario puede crear, editar y cambiar estado, pero no borrar
                'add_consulta', 'view_consulta', 'change_consulta',
                'add_analisis', 'view_analisis', 'change_analisis',
                'add_cirugia', 'view_cirugia', 'change_cirugia',
                'add_urgencia', 'view_urgencia', 'change_urgencia',
                # Permisos para ver panel y reportes
                'view_panel_admin', 'view_reportes',
            ]
        },
        'auxiliar': {
            'is_staff': True,
            'is_superuser': False,
            'permisos': [
                # El auxiliar solo puede ver, no tocar nada
                'view_consulta',
                'view_analisis',
                'view_cirugia',
                'view_urgencia',
            ]
        },
        'recepcionista': {
            'is_staff': True,
            'is_superuser': False,
            'permisos': [
                # La recepcionista puede gestionar citas (crear, ver, modificar, eliminar, cambiar estado)
                'add_consulta', 'view_consulta', 'change_consulta', 'delete_consulta',
                'add_analisis', 'view_analisis', 'change_analisis', 'delete_analisis',
                'add_cirugia', 'view_cirugia', 'change_cirugia', 'delete_cirugia',
                'add_urgencia', 'view_urgencia', 'change_urgencia', 'delete_urgencia',
                # Permisos para notificaciones
                'view_notificacion', 'change_notificacion',
                # Puede ver usuarios para atención al cliente
                'view_user',
                # Puede ver panel de admin para gestionar citas
                'view_panel_admin',
            ]
        },
        'cliente': {
            'is_staff': False,
            'is_superuser': False,
            'permisos': []  # Cliente no tiene permisos de admin
        }
    }
    
    # Guardamos la config segun el rol
    config = permisos_por_rol.get(rol, permisos_por_rol['cliente'])
    
    # Marcamos si es del personal o no
    usuario.is_staff = config['is_staff']
    usuario.is_superuser = config['is_superuser']
    usuario.save()
    
    # Le damos los permisos
    for perm_codename in config['permisos']:
        try:
            perm = Permission.objects.filter(codename=perm_codename).first()
            if perm:
                usuario.user_permissions.add(perm)
        except Exception:
            pass  # Si hay error, continuamos
    
    # Lo metemos en su grupo
    if rol in ['veterinario', 'auxiliar', 'recepcionista', 'admin']:
        grupo_mapping = {
            'veterinario': 'Veterinarios',
            'auxiliar': 'Auxiliares',
            'recepcionista': 'Recepcionistas',
            'admin': 'Administradores',
        }
        try:
            grupo = Group.objects.get(name=grupo_mapping[rol])
            usuario.groups.add(grupo)
        except Group.DoesNotExist:
            pass


# Funcion para usar manualmente si hace falta
def asignar_permisos_a_usuario(usuario, rol):
    # Guardamos el rol para que se activen los permisos
    if hasattr(usuario, 'perfil'):
        usuario.perfil.rol = rol
        usuario.perfil.save()
        return True
    return False


# Para crear los grupos a mano desde la consola de Django
def crear_grupos_y_permisos():
    from django.contrib.auth.models import Group
    
    grupos = {
        'Veterinarios': [
            'add_consulta', 'view_consulta', 'change_consulta',
            'add_analisis', 'view_analisis', 'change_analisis',
            'add_cirugia', 'view_cirugia', 'change_cirugia',
            'add_urgencia', 'view_urgencia', 'change_urgencia',
            'view_panel_admin', 'view_reportes',
        ],
        'Auxiliares': [
            'view_consulta', 'view_analisis', 'view_cirugia', 'view_urgencia',
        ],
        'Recepcionistas': [
            'add_consulta', 'view_consulta', 'change_consulta', 'delete_consulta',
            'add_analisis', 'view_analisis', 'change_analisis', 'delete_analisis',
            'add_cirugia', 'view_cirugia', 'change_cirugia', 'delete_cirugia',
            'add_urgencia', 'view_urgencia', 'change_urgencia', 'delete_urgencia',
            'view_notificacion', 'change_notificacion',
            'view_user', 'view_panel_admin',
        ],
        'Administradores': [
            'add_user', 'view_user', 'change_user', 'delete_user',
            'add_consulta', 'view_consulta', 'change_consulta', 'delete_consulta',
            'add_analisis', 'view_analisis', 'change_analisis', 'delete_analisis',
            'add_cirugia', 'view_cirugia', 'change_cirugia', 'delete_cirugia',
            'add_urgencia', 'view_urgencia', 'change_urgencia', 'delete_urgencia',
            'view_notificacion', 'change_notificacion', 'delete_notificacion',
            'view_panel_admin', 'view_reportes',
        ],
    }
    
    for nombre_grupo, permisos in grupos.items():
        group, created = Group.objects.get_or_create(name=nombre_grupo)
        
        for perm_codename in permisos:
            try:
                # Buscar permiso específico por codename y app
                if 'notificacion' in perm_codename:
                    from django.contrib.contenttypes.models import ContentType
                    from notificaciones.models import Notificacion
                    content_type = ContentType.objects.get_for_model(Notificacion)
                    perm = Permission.objects.get(codename=perm_codename, content_type=content_type)
                else:
                    perm = Permission.objects.get(codename=perm_codename)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                print(f"Permiso no encontrado: {perm_codename}")
        
        print(f"Grupo {nombre_grupo} listo con {len(permisos)} permisos")
    
    # Configurar permisos de notificaciones
    configurar_permisos_notificaciones()


def crear_permisos_personalizados():
    content_type = ContentType.objects.get_for_model(Perfil)
    
    permisos = [
        ('view_panel_admin', 'Puede ver panel de administración'),
        ('view_reportes', 'Puede ver reportes y estadísticas'),
        ('gestionar_citas', 'Puede gestionar todas las citas'),
        ('gestionar_usuarios', 'Puede gestionar usuarios del sistema'),
    ]
    
    for codename, name in permisos:
        perm, created = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=content_type,
        )
        if created:
            print(f"Permiso personalizado creado: {codename}")


def configurar_permisos_notificaciones():
    """Configurar permisos de notificaciones para grupos"""
    from django.contrib.auth.models import Group
    from django.contrib.contenttypes.models import ContentType
    from notificaciones.models import Notificacion
    
    print("Configurando permisos de notificaciones...")
    
    # Obtener content type de notificaciones
    content_type = ContentType.objects.get_for_model(Notificacion)
    
    # Obtener permisos existentes
    permisos = Permission.objects.filter(content_type=content_type)
    print(f"Permisos encontrados: {[p.codename for p in permisos]}")
    
    # Crear grupos si no existen
    grupos_necesarios = ['Recepcionistas', 'Administradores']
    
    for nombre_grupo in grupos_necesarios:
        grupo, created = Group.objects.get_or_create(name=nombre_grupo)
        if created:
            print(f"✓ Grupo creado: {nombre_grupo}")
        else:
            print(f"- Grupo ya existía: {nombre_grupo}")
    
    # Asignar permisos a recepcionistas
    grupo_recepcionistas = Group.objects.get(name='Recepcionistas')
    for perm in permisos:
        if perm.codename in ['view_notificacion', 'change_notificacion']:
            grupo_recepcionistas.permissions.add(perm)
            print(f"✓ Añadido {perm.codename} a Recepcionistas")
    
    # Asignar todos los permisos a administradores
    grupo_admins = Group.objects.get(name='Administradores')
    for perm in permisos:
        grupo_admins.permissions.add(perm)
        print(f"✓ Añadido {perm.codename} a Administradores")
    
    print("¡Permisos de notificaciones configurados correctamente!")
