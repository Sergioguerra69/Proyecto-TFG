# Formularios: usamos ModelForm para que Django genere los campos automaticamente
# Este archivo sirve para crear el formulario que el usuario verá en la web
from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        # Elegimos los campos que queremos mostrar
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        # Podemos añadir clases de Bootstrap directamente aquí
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '¿En qué podemos ayudarte?'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe aquí tu duda...'}),
        }
