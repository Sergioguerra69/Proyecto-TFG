# Formularios: usamos ModelForm para que Django genere los campos automaticamente
# users/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

# Clase CSS para todos los campos
CLASE_INPUT = 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 transition-all duration-300'

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        label="Nombre",
        widget=forms.TextInput(attrs={'class': CLASE_INPUT})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        label="Apellidos",
        widget=forms.TextInput(attrs={'class': CLASE_INPUT})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': CLASE_INPUT})
    )
    telefono = forms.CharField(
        max_length=15, 
        required=False,
        widget=forms.TextInput(attrs={'class': CLASE_INPUT})
    )
    direccion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': CLASE_INPUT}), 
        required=False
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': CLASE_INPUT})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': CLASE_INPUT})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': CLASE_INPUT})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'telefono', 'direccion', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplicar clase CSS a TODOS los campos (incluyendo password1 y password2)
        for field in self.fields.values():
            field.widget.attrs.update({'class': CLASE_INPUT})
        
        # Personalizar etiquetas
        self.fields['username'].label = "Nombre de usuario"
        self.fields['email'].label = "Correo electrónico"
        self.fields['telefono'].label = "Teléfono"
        self.fields['direccion'].label = "Dirección"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"
    
    def save(self, commit=True):
        user = super().save(commit)
        # Guardar nombre y apellido del usuario
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        
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