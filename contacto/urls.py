# URLs: enlazamos las rutas del navegador con las funciones de views.py
# Este archivo sirve para las rutas de la sección de contacto
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacto, name='contacto'),
]
