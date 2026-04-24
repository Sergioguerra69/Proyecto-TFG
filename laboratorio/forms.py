# Formularios: usamos ModelForm para que Django genere los campos automaticamente
from django import forms
from .models import Analisis

class AnalisisForm(forms.ModelForm):
    class Meta:
        model = Analisis
        fields = ['nombre', 'paciente', 'fecha', 'resultado', 'notas', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
