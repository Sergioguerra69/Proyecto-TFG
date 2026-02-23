# Formularios: usamos ModelForm para que Django genere los campos automaticamente
from django import forms
from .models import Urgencia

class UrgenciaForm(forms.ModelForm):
    class Meta:
        model = Urgencia
        fields = ['paciente', 'prioridad', 'descripcion', 'estado']
