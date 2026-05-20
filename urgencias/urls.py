# URLs de urgencias
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_urgencias, name='lista_urgencias'),
    path('nueva/', views.crear_urgencia, name='crear_urgencia'),
    path('editar/<int:id>/', views.editar_urgencia, name='editar_urgencia'),
    path('eliminar/<int:id>/', views.eliminar_urgencia, name='eliminar_urgencia'),
    path('estado/<int:id>/', views.actualizar_estado_urgencia, name='actualizar_estado_urgencia'),
    path('prioridad/<int:id>/', views.actualizar_prioridad_urgencia, name='actualizar_prioridad_urgencia'),
    path('pdf/<int:urgencia_id>/', views.pdf_urgencia, name='pdf_urgencia'),
]
