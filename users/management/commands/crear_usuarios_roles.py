#!/usr/bin/env python
"""
Comando de Django para crear usuarios de prueba con diferentes roles.
Ejecutar: python manage.py crear_usuarios_roles
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Perfil

# Datos de los usuarios a crear
USUARIOS_ROLES = [
    {
        'username': 'admin',
        'email': 'admin@vetct.com',
        'password': 'admin123',
        'rol': 'admin',
        'nombre': 'Administrador',
        'telefono': '600000000'
    },
    {
        'username': 'veterinario1',
        'email': 'vet1@vetct.com',
        'password': 'vet123',
        'rol': 'veterinario',
        'nombre': 'Dr. García',
        'telefono': '600000001'
    },
    {
        'username': 'recepcionista1',
        'email': 'recepcion1@vetct.com',
        'password': 'recepcion123',
        'rol': 'recepcionista',
        'nombre': 'María López',
        'telefono': '600000002'
    },
    {
        'username': 'cliente1',
        'email': 'cliente1@vetct.com',
        'password': 'cliente123',
        'rol': 'cliente',
        'nombre': 'Juan Pérez',
        'telefono': '600000003'
    },
]

class Command(BaseCommand):
    help = 'Crear usuarios de prueba con diferentes roles'

    def handle(self, *args, **options):
        self.stdout.write('Creando usuarios de prueba...')
        
        for usuario_data in USUARIOS_ROLES:
            username = usuario_data['username']
            
            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'El usuario {username} ya existe'))
                continue
            
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=usuario_data['email'],
                password=usuario_data['password']
            )
            
            # Crear perfil
            perfil = Perfil.objects.create(
                user=user,
                rol=usuario_data['rol'],
                nombre=usuario_data['nombre'],
                telefono=usuario_data['telefono']
            )
            
            # Asignar permisos según el rol
            from users.signals import asignar_permisos_usuario
            asignar_permisos_usuario(user, usuario_data['rol'])
            
            self.stdout.write(self.style.SUCCESS(f'✓ Usuario {username} creado con rol {usuario_data["rol"]}'))
        
        self.stdout.write(self.style.SUCCESS('¡Usuarios de prueba creados correctamente!'))
