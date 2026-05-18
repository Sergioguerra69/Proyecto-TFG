# URLs de notificaciones
from django.urls import path
from . import views

urlpatterns = [
    # Paneles de trabajo
    path('recepcion/', views.panel_recepcion, name='panel_recepcion'),
    
    # Panel de veterinarios
    path('veterinario/', views.panel_veterinario, name='panel_veterinario'),
    path('mis-notificaciones/', views.mis_notificaciones, name='mis_notificaciones'),
    
    # Configuración de permisos
    path('configurar-permisos/', views.configurar_permisos, name='configurar_permisos'),
    
    # Gestión de citas - Panel veterinario
    path('ver/<str:tipo>/<int:cita_id>/', views.ver_cita, name='ver_cita'),
    path('aceptar/<str:tipo>/<int:cita_id>/', views.aceptar_cita, name='aceptar_cita'),
    path('completar/<str:tipo>/<int:cita_id>/', views.completar_cita, name='completar_cita'),
    path('rechazar/<str:tipo>/<int:cita_id>/', views.rechazar_cita, name='rechazar_cita'),
    path('cancelar/<str:tipo>/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('eliminar/<str:tipo>/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    path('crear/', views.crear_cita, name='crear_cita'),
    
    # Gestión de citas - Panel recepción
    path('aceptar-recepcion/<str:tipo>/<int:cita_id>/', views.aceptar_cita_recepcion, name='aceptar_cita_recepcion'),
    path('rechazar-recepcion/<str:tipo>/<int:cita_id>/', views.rechazar_cita_recepcion, name='rechazar_cita_recepcion'),
    
    # Gestión de solicitudes (antiguo)
    path('aceptar-solicitud/<int:notificacion_id>/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('rechazar-solicitud/<int:notificacion_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),
]
