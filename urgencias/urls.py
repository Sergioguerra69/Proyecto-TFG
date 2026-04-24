# URLs: enlazamos las rutas del navegador con las funciones de views.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_urgencias, name='lista_urgencias'),
    path('nueva/', views.crear_urgencia, name='crear_urgencia'),
    path('editar/<int:id>/', views.editar_urgencia, name='editar_urgencia'),
    path('eliminar/<int:id>/', views.eliminar_urgencia, name='eliminar_urgencia'),
    path('estado/<int:id>/', views.actualizar_estado_urgencia, name='actualizar_estado_urgencia'),
]
