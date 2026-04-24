# Formularios: usamos ModelForm para que Django genere los campos automaticamente
from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'veterinario', 'fecha', 'motivo', 'diagnostico', 'estado']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
