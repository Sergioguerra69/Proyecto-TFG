# Formularios para urgencias
from django import forms
from .models import Urgencia

class UrgenciaForm(forms.ModelForm):
    class Meta:
        model = Urgencia
        fields = ['paciente', 'solicita_prioridad', 'descripcion']

class UrgenciaVeterinarioForm(forms.ModelForm):
    class Meta:
        model = Urgencia
        fields = ['paciente', 'solicita_prioridad', 'prioridad', 'descripcion', 'estado']
