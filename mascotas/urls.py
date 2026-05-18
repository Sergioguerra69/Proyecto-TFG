from django.urls import path
from . import views

app_name = 'mascotas'

urlpatterns = [
    path('<int:mascota_id>/historial/', views.historial_clinico, name='historial'),
]
