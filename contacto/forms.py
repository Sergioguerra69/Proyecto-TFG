# Formularios para el sistema de contacto
from django import forms
from .models import FormularioContacto, MensajeCliente, AsignacionSolicitud

# Estilo CSS para los campos del formulario
CLASE_INPUT = 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 transition-all duration-300'

class FormularioContactoForm(forms.ModelForm):
    class Meta:
        model = FormularioContacto
        fields = ['nombre', 'apellidos', 'dni', 'email', 'telefono', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': CLASE_INPUT,
                'placeholder': 'Nombre'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': CLASE_INPUT,
                'placeholder': 'Apellidos'
            }),
            'dni': forms.TextInput(attrs={
                'class': CLASE_INPUT,
                'placeholder': 'DNI'
            }),
            'email': forms.EmailInput(attrs={
                'class': CLASE_INPUT,
                'placeholder': 'Correo electrónico'
            }),
            'telefono': forms.TextInput(attrs={
                'class': CLASE_INPUT,
                'placeholder': 'Teléfono (opcional)'
            }),
            'asunto': forms.TextInput(attrs={
                'class': CLASE_INPUT,
                'placeholder': 'Asunto del mensaje'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': CLASE_INPUT,
                'rows': 5,
                'placeholder': 'Escribe tu mensaje aquí...'
            })
        }

class RespuestaContactoForm(forms.Form):
    contenido = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': CLASE_INPUT,
            'rows': 4,
            'placeholder': 'Escribe tu respuesta aquí...'
        })
    )

class MensajeClienteForm(forms.ModelForm):
    class Meta:
        model = MensajeCliente
        fields = ['nombre', 'email', 'telefono', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': CLASE_INPUT,
                'placeholder': 'Nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': CLASE_INPUT,
                'placeholder': 'Correo electrónico'
            }),
            'telefono': forms.TextInput(attrs={
                'class': CLASE_INPUT,
                'placeholder': 'Teléfono (opcional)'
            }),
            'asunto': forms.TextInput(attrs={
                'class': CLASE_INPUT,
                'placeholder': 'Asunto de tu duda'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': CLASE_INPUT,
                'rows': 5,
                'placeholder': 'Describe detalladamente tu duda o consulta...'
            })
        }

class RespuestaMensajeForm(forms.Form):
    contenido = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': CLASE_INPUT,
            'rows': 4,
            'placeholder': 'Escribe tu respuesta aquí...'
        })
    )

class AsignacionSolicitudForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo usuarios que son veterinarios
        from django.contrib.auth.models import User
        self.fields['veterinario'].queryset = User.objects.filter(perfil__rol='veterinario')
    
    class Meta:
        model = AsignacionSolicitud
        fields = ['veterinario', 'notas_asignacion']
        widgets = {
            'veterinario': forms.Select(attrs={
                'class': CLASE_INPUT,
            }),
            'notas_asignacion': forms.Textarea(attrs={
                'class': CLASE_INPUT,
                'rows': 3,
                'placeholder': 'Notas adicionales para el veterinario...'
            })
        }
