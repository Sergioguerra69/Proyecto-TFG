# URLs: enlazamos las rutas del navegador con las funciones de views.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_estetica, name='lista_estetica'),
    path('nueva/', views.crear_estetica, name='crear_estetica'),
    path('estado/<int:id>/', views.actualizar_estado_estetica, name='actualizar_estado_estetica'),
]
