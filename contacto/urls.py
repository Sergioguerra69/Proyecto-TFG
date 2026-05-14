# URLs para el sistema de contacto
from django.urls import path
from . import views

urlpatterns = [
    # Formulario de contacto público
    path('contacto/', views.contacto_publico, name='contacto_publico'),
    # URL de compatibilidad para enlaces antiguos
    path('', views.contacto_publico, name='contacto'),
    
    # Panel de recepcionista
    path('panel-recepcionista/', views.panel_contactos_recepcionista, name='panel_contactos_recepcionista'),
    
    # Panel de mensajes de clientes
    path('panel-mensajes/', views.panel_mensajes_recepcionista, name='panel_mensajes_recepcionista'),
    
    # Ver y responder mensaje de cliente
    path('mensaje/<int:mensaje_id>/', views.ver_mensaje_cliente, name='ver_mensaje_cliente'),
    
    # Marcar mensaje como leído
    path('mensaje/<int:mensaje_id>/marcar-leido/', views.marcar_mensaje_leido, name='marcar_mensaje_leido'),
    
    # Cerrar mensaje
    path('mensaje/<int:mensaje_id>/cerrar/', views.cerrar_mensaje, name='cerrar_mensaje'),
    
    # Asignar solicitud a veterinario
    path('asignar/<int:formulario_id>/', views.asignar_solicitud, name='asignar_solicitud'),
    
    # Gestionar solicitud para veterinarios
    path('gestionar-solicitud/<int:notificacion_id>/', views.gestionar_solicitud_veterinario, name='gestionar_solicitud_veterinario'),
    
    # Panel de veterinarios
    path('panel-veterinario/', views.panel_veterinario, name='panel_veterinario'),
    
    # Ver formulario de contacto
    path('formulario-contacto/<int:formulario_id>/', views.ver_formulario_contacto, name='ver_formulario_contacto'),
    
    # Ver solicitud asignada
    path('solicitud-asignada/<int:asignacion_id>/', views.ver_solicitud_asignada, name='ver_solicitud_asignada'),
    
    # Notificaciones del veterinario
    path('notificaciones-veterinario/', views.ver_notificaciones_veterinario, name='ver_notificaciones_veterinario'),
    
    # Responder formulario
    path('responder/<int:formulario_id>/', views.responder_formulario, name='responder_formulario'),
    
    # Panel personal del cliente
    path('panel-cliente/', views.panel_contactos_cliente, name='panel_contactos_cliente'),
    
    # Responder a una respuesta (cliente)
    path('responder-respuesta/<int:formulario_id>/', views.responder_respuesta, name='responder_respuesta'),
    
    # Ver detalles de un formulario
    path('ver/<int:formulario_id>/', views.ver_formulario, name='ver_formulario'),
]
