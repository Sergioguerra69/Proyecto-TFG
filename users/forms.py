# Formularios: usamos ModelForm para que Django genere los campos automaticamente
# users/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=15, required=False)
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'telefono', 'direccion'] # Definimos el orden de los campos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bucle para añadir clases de Bootstrap manualmente a cada campo
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit)
        # Verificamos si el perfil ya existe (o lo creamos)
        Perfil.objects.update_or_create(
            usuario=user,
            defaults={
                'telefono': self.cleaned_data.get('telefono', ''),
                'direccion': self.cleaned_data.get('direccion', '')
            }
        )
        return user

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefono', 'direccion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})