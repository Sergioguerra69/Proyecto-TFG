# Formularios para análisis de laboratorio
from django import forms
from .models import Analisis

class AnalisisForm(forms.ModelForm):
    class Meta:
        model = Analisis
        fields = ['nombre', 'paciente', 'fecha', 'hora', 'resultado', 'notas', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
