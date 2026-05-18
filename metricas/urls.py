from django.urls import path
from . import views

app_name = 'metricas'

urlpatterns = [
    path('dashboard/', views.dashboard_analitico, name='dashboard'),
]
