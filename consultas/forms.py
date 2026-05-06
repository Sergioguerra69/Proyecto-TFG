# Formularios para consultas veterinarias
from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    """Formulario para crear y editar consultas"""
    class Meta:
        model = Consulta
        # Campos que se mostrarán en el formulario
        fields = ['paciente', 'veterinario', 'fecha', 'motivo', 'diagnostico', 'estado']
        
        # Personalizar cómo se ven los campos
        widgets = {
            # Selector de fecha y hora
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
