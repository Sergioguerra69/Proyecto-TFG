# Template filters para notificaciones
from django import template

register = template.Library()

@register.filter
def tipo_icono(tipo):
    """Devuelve el icono de FontAwesome según el tipo"""
    iconos = {
        'consulta': 'fa-stethoscope',
        'analisis': 'fa-flask',
        'cirugia': 'fa-procedures',
        'urgencia': 'fa-ambulance',
    }
    return iconos.get(tipo, 'fa-bell')

@register.filter
def tipo_color(tipo):
    """Devuelve el color según el tipo"""
    colores = {
        'consulta': 'blue',
        'analisis': 'green',
        'cirugia': 'purple',
        'urgencia': 'red',
    }
    return colores.get(tipo, 'gray')
