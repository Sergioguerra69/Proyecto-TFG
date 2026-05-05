# -*- coding: utf-8 -*-
"""
Comando para configurar grupos y notificaciones.
Crea los grupos necesarios y asigna usuarios según su rol.
Uso: python manage.py configurar_grupos_notificaciones
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from users.models import Perfil


class Command(BaseCommand):
    help = 'Configura grupos para notificaciones y asigna usuarios'

    def handle(self, *args, **options):
        self.stdout.write('Configurando grupos para notificaciones...')
        
        # Crear grupos si no existen
        grupos_necesarios = ['Veterinarios', 'Recepcionistas', 'Auxiliares', 'Administradores']
        for nombre in grupos_necesarios:
            grupo, created = Group.objects.get_or_create(name=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo creado: {nombre}'))
            else:
                self.stdout.write(f'- Grupo ya existía: {nombre}')
        
        # Asignar usuarios a grupos según su rol
        perfiles = Perfil.objects.all()
        asignados = 0
        
        for perfil in perfiles:
            usuario = perfil.usuario
            rol = perfil.rol
            
            # Mapeo de roles a grupos
            grupo_mapping = {
                'veterinario': 'Veterinarios',
                'recepcionista': 'Recepcionistas',
                'auxiliar': 'Auxiliares',
                'admin': 'Administradores',
            }
            
            if rol in grupo_mapping:
                grupo_nombre = grupo_mapping[rol]
                try:
                    grupo = Group.objects.get(name=grupo_nombre)
                    usuario.groups.add(grupo)
                    asignados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {usuario.username} → {grupo_nombre}')
                    )
                except Group.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Grupo {grupo_nombre} no encontrado')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n¡Configuración completa! {asignados} usuarios asignados a grupos.')
        )
        self.stdout.write('\nAhora las notificaciones funcionarán correctamente:')
        self.stdout.write('- Usuario crea cita → Notificación a Recepcionistas')
        self.stdout.write('- Recepcionista acepta → Notificación a Veterinarios')
