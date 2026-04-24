# Formularios: usamos ModelForm para que Django genere los campos automaticamente
from django import forms
from .models import ServicioEstetica

class EsteticaForm(forms.ModelForm):
    class Meta:
        model = ServicioEstetica
        fields = ['paciente', 'tipo_servicio', 'fecha', 'observaciones', 'estado']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
