# URLs: enlazamos las rutas del navegador con las funciones de views.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_consultas, name='lista_consultas'),
    path('nueva/', views.crear_consulta, name='crear_consulta'),
    path('estado/<int:id>/', views.actualizar_estado_consulta, name='actualizar_estado_consulta'),
]
