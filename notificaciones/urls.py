# URLs: enlazamos las rutas del navegador con las funciones de views.py
from django.urls import path
from . import views

urlpatterns = [
    # Panel de recepción
    path('recepcion/', views.panel_recepcion, name='panel_recepcion'),
    
    # Panel de veterinarios
    path('veterinario/', views.panel_veterinario, name='panel_veterinario'),
    path('mis-notificaciones/', views.mis_notificaciones, name='mis_notificaciones'),
    
    # Configurar permisos (solo admin)
    path('configurar-permisos/', views.configurar_permisos, name='configurar_permisos'),
    
    # Gestionar citas
    path('aceptar/<str:tipo>/<int:cita_id>/', views.aceptar_cita, name='aceptar_cita'),
    path('rechazar/<str:tipo>/<int:cita_id>/', views.rechazar_cita, name='rechazar_cita'),
    path('eliminar/<str:tipo>/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    path('crear/', views.crear_cita, name='crear_cita'),
    
    # Gestionar solicitudes (antiguo)
    path('aceptar-solicitud/<int:notificacion_id>/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('rechazar-solicitud/<int:notificacion_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),
]
