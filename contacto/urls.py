# URLs de contacto
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacto, name='contacto'),
]
