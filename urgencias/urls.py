# URLs: enlazamos las rutas del navegador con las funciones de views.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_urgencias, name='lista_urgencias'),
    path('nueva/', views.crear_urgencia, name='crear_urgencia'),
    path('estado/<int:id>/', views.actualizar_estado_urgencia, name='actualizar_estado_urgencia'),
]
