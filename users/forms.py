# Formularios de usuarios - registro y perfiles
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

# Estilo CSS para los campos del formulario
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
        
        # Aplicar estilo CSS a todos los campos
        for field in self.fields.values():
            field.widget.attrs.update({'class': CLASE_INPUT})
        
        # Cambiar nombres de los campos
        self.fields['username'].label = "Nombre de usuario"
        self.fields['email'].label = "Correo electrónico"
        self.fields['telefono'].label = "Teléfono"
        self.fields['direccion'].label = "Dirección"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"
    
    def save(self, commit=True):
        user = super().save(commit)
        # Guardar datos del usuario
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        
        # Crear o actualizar perfil del usuario
        Perfil.objects.update_or_create(
            usuario=user,
            defaults={
                'telefono': self.cleaned_data.get('telefono', ''),
                'direccion': self.cleaned_data.get('direccion', '')
            }
        )
        return user

class PerfilForm(forms.ModelForm):
    # Campos de la cuenta de usuario
    first_name = forms.CharField(
        label="Nombre",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        label="Apellido",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Tu apellido'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Tu correo electrónico'
        })
    )
    
    # Campos del perfil
    telefono = forms.CharField(
        label="Teléfono",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Tu número de teléfono'
        })
    )
    direccion = forms.CharField(
        label="Dirección",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'rows': 3,
            'placeholder': 'Tu dirección completa'
        })
    )
    especialidad = forms.CharField(
        label="Especialidad",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Tu especialidad (solo para veterinarios)'
        })
    )

    class Meta:
        model = Perfil
        fields = []  # Los campos se definen manualmente arriba

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar campos con valores actuales del usuario
        if self.instance and hasattr(self.instance, 'usuario'):
            user = self.instance.usuario
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['telefono'].initial = self.instance.telefono
            self.fields['direccion'].initial = self.instance.direccion
            self.fields['especialidad'].initial = self.instance.especialidad
            
            # Ocultar especialidad si no es veterinario
            if self.instance.rol != 'veterinario':
                self.fields['especialidad'].widget.attrs['readonly'] = True
                self.fields['especialidad'].widget.attrs['placeholder'] = 'Solo disponible para veterinarios'
        
        # Añadir clases CSS adicionales
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] += ' focus:ring-1 focus:ring-blue-500 focus:ring-opacity-5'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and self.instance and hasattr(self.instance, 'usuario'):
            # Verificar que el email no esté en uso por otro usuario
            existing_user = User.objects.filter(email=email).exclude(pk=self.instance.usuario.pk).first()
            if existing_user:
                raise forms.ValidationError("Este email ya está en uso por otro usuario")
        return email