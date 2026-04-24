# Formularios: usamos ModelForm para que Django genere los campos automaticamente
from django import forms
from .models import Cirugia

class CirugiaForm(forms.ModelForm):
    class Meta:
        model = Cirugia
        fields = ['paciente', 'tipo_cirugia', 'fecha', 'estado', 'quirofano']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
