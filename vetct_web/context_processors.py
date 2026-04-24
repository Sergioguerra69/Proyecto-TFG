"""
PROCESADOR DE CONTEXTO PARA VETCT
Este archivo pasa información automáticamente a TODAS las plantillas.
Es como un asistente que siempre está disponible.
"""

from django.conf import settings

def vetct_info(request):
    """
    Context processor que pasa la información de la clínica a todas las templates
    """
    # Obtengo la info de la clínica desde settings
    info = settings.VETCT_INFO
    redes = info.get('REDES_SOCIALES', {})
    
    return {
        # Información básica (usando las claves exactas de settings.py)
        'clinic_name': info['NOMBRE_EMPRESA'],
        'clinic_full_name': info['NOMBRE_COMPLETO'],
        'clinic_slogan': 'Cuidando a tus mejores amigos',  # Añadido manualmente
        
        # Datos de contacto
        'clinic_phone': info['TELEFONO_PRINCIPAL'],
        'emergency_phone': info['TELEFONO_URGENCIAS'],
        'clinic_email': info['EMAIL_CONTACTO'],
        'clinic_address': info['DIRECCION'],
        
        # Horarios
        'schedule_normal': info['HORARIO_NORMAL'],
        'schedule_weekend': info['HORARIO_FIN_SEMANA'],
        
        # Redes sociales
        'facebook_url': redes.get('facebook', '#'),
        'instagram_url': redes.get('instagram', '#'),
        'twitter_url': redes.get('twitter', '#'),
    }