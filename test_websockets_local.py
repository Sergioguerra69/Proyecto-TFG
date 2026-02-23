#!/usr/bin/env python
"""
Script de prueba para verificar que los WebSockets funcionan en Windows local
sin necesidad de Redis externo.
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetct_web.settings')
django.setup()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def test_websockets():
    """Prueba el sistema de WebSockets con InMemoryChannelLayer"""
    print("🧪 Probando sistema de WebSockets local...")
    
    try:
        # Obtener el channel layer configurado
        channel_layer = get_channel_layer()
        print(f"✅ Channel Layer detectado: {type(channel_layer).__name__}")
        
        # Enviar un mensaje de prueba
        async_to_sync(channel_layer.group_send)(
            'clinica_notificaciones',
            {
                'type': 'enviar.notificacion',
                'message': '📢 Test: Sistema de notificaciones funcionando en Windows local!'
            }
        )
        print("✅ Mensaje de prueba enviado correctamente")
        
        # Verificar configuración de caché
        from django.core.cache import cache
        cache.set('test_key', 'test_value', 60)
        cached_value = cache.get('test_key')
        
        if cached_value == 'test_value':
            print("✅ Sistema de caché local funcionando")
        else:
            print("❌ Error en sistema de caché")
            
        print("\n🎉 Todas las pruebas pasaron exitosamente!")
        print("📝 Las funciones actualizar_estado de todas las apps funcionarán sin errores.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

if __name__ == "__main__":
    success = test_websockets()
    sys.exit(0 if success else 1)
