from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Configura grupos y permisos para veterinarios y recepcionistas'

    def handle(self, *args, **options):
        # Crear grupos si no existen
        veterinarios_group, created = Group.objects.get_or_create(name='veterinarios')
        recepcionistas_group, created = Group.objects.get_or_create(name='recepcionistas')
        
        # Obtener permisos de notificaciones
        notificacion_content_type = ContentType.objects.get(app_label='notificaciones', model='notificacion')
        
        # Permisos para veterinarios
        vet_permissions = Permission.objects.filter(
            content_type=notificacion_content_type,
            codename__in=['view_notificacion', 'add_notificacion']
        )
        
        # Permisos para recepcionistas
        recep_permissions = Permission.objects.filter(
            content_type=notificacion_content_type
        )
        
        # Asignar permisos a los grupos
        veterinarios_group.permissions.set(vet_permissions)
        recepcionistas_group.permissions.set(recep_permissions)
        
        self.stdout.write(
            self.style.SUCCESS('Grupos y permisos configurados correctamente')
        )
        
        # Mostrar usuarios en cada grupo
        self.stdout.write('Veterinarios en el grupo:')
        for user in veterinarios_group.user_set.all():
            self.stdout.write(f'  - {user.username}')
            
        self.stdout.write('Recepcionistas en el grupo:')
        for user in recepcionistas_group.user_set.all():
            self.stdout.write(f'  - {user.username}')
