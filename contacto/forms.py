# Formularios de contacto
from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        # Campos que se mostrarán
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        # Estilo Bootstrap para los campos
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '¿En qué podemos ayudarte?'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe aquí tu duda...'}),
        }
