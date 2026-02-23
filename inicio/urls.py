# URLs: enlazamos las rutas del navegador con las funciones de views.py

from django.urls import path
from . import views

app_name = 'inicio'

urlpatterns = [
    path('', views.home, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('equipo/', views.equipo, name='equipo'),
]