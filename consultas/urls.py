# URLs de consultas veterinarias
from django.urls import path
from . import views

urlpatterns = [
    # Lista de todas las consultas
    path('', views.lista_consultas, name='lista_consultas'),
    
    # Crear nueva consulta
    path('nueva/', views.crear_consulta, name='crear_consulta'),
    
    # Editar consulta existente
    path('editar/<int:id>/', views.editar_consulta, name='editar_consulta'),
    
    # Eliminar consulta
    path('eliminar/<int:id>/', views.eliminar_consulta, name='eliminar_consulta'),
    
    # Cambiar estado de la consulta
    path('estado/<int:id>/', views.actualizar_estado_consulta, name='actualizar_estado_consulta'),
]
