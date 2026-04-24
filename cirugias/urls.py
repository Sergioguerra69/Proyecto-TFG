# URLs: enlazamos las rutas del navegador con las funciones de views.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cirugias, name='lista_cirugias'),
    path('nueva/', views.crear_cirugia, name='crear_cirugia'),
    path('editar/<int:id>/', views.editar_cirugia, name='editar_cirugia'),
    path('eliminar/<int:id>/', views.eliminar_cirugia, name='eliminar_cirugia'),
    path('estado/<int:id>/', views.actualizar_estado_cirugia, name='actualizar_estado_cirugia'),
]
