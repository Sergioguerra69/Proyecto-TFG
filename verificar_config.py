#!/usr/bin/env python
"""
Script para verificar la configuración de Redis/WebSockets
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetct_web.settings')
django.setup()

from django.conf import settings

print("🔍 Verificando configuración de Django...")
print(f"DEBUG: {settings.DEBUG}")
print(f"DATABASES: {settings.DATABASES['default']['ENGINE']}")

print("\n🔍 Verificando configuración de CACHES...")
print(f"CACHE BACKEND: {settings.CACHES['default']['BACKEND']}")

print("\n🔍 Verificando configuración de CHANNEL_LAYERS...")
print(f"CHANNEL BACKEND: {settings.CHANNEL_LAYERS['default']['BACKEND']}")

# Verificar variable de entorno REDIS_URL
redis_url = os.environ.get('REDIS_URL', 'NO DEFINIDA')
print(f"\n🔍 Variable de entorno REDIS_URL: {redis_url}")

if 'InMemory' in settings.CHANNEL_LAYERS['default']['BACKEND']:
    print("\n✅ Configuración LOCAL detectada (InMemoryChannelLayer)")
else:
    print("\n⚠️ Configuración REDIS detectada")
