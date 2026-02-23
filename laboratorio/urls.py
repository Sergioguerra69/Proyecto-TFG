# URLs: enlazamos las rutas del navegador con las funciones de views.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_analisis, name='lista_analisis'),
    path('nuevo/', views.crear_analisis, name='crear_analisis'),
    path('estado/<int:id>/', views.actualizar_estado_analisis, name='actualizar_estado_analisis'),
]
