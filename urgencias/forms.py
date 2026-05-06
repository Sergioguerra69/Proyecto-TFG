# Formularios para urgencias
from django import forms
from .models import Urgencia

class UrgenciaForm(forms.ModelForm):
    class Meta:
        model = Urgencia
        fields = ['paciente', 'prioridad', 'descripcion', 'estado']
