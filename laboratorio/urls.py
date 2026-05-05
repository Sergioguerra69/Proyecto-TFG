# URLs de análisis de laboratorio
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_analisis, name='lista_analisis'),
    path('nuevo/', views.crear_analisis, name='crear_analisis'),
    path('editar/<int:id>/', views.editar_analisis, name='editar_analisis'),
    path('eliminar/<int:id>/', views.eliminar_analisis, name='eliminar_analisis'),
    path('estado/<int:id>/', views.actualizar_estado_analisis, name='actualizar_estado_analisis'),
]
