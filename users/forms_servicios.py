# Formularios para que los usuarios soliciten servicios
# users/forms_servicios.py
from django import forms
from django.contrib.auth.models import User
from consultas.models import Consulta
from laboratorio.models import Analisis
from cirugias.models import Cirugia
from urgencias.models import Urgencia

class SolicitudConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'tipo_animal', 'tipo_animal_otro', 'fecha', 'motivo']
        widgets = {
            'paciente': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'placeholder': 'Nombre de su mascota'
            }),
            'tipo_animal': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'id': 'tipo_animal_select'
            }),
            'tipo_animal_otro': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'placeholder': 'Especifique qué animal es',
                'id': 'tipo_animal_otro_input'
            }),
            'fecha': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'type': 'datetime-local'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'rows': 4,
                'placeholder': 'Describa los síntomas o motivo de la consulta'
            })
        }

class SolicitudAnalisisForm(forms.ModelForm):
    class Meta:
        model = Analisis
        fields = ['nombre', 'paciente', 'tipo_animal', 'tipo_animal_otro', 'fecha', 'notas']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'placeholder': 'Ej: Hemograma, Análisis de orina'
            }),
            'paciente': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'placeholder': 'Nombre de su mascota'
            }),
            'tipo_animal': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'id': 'tipo_animal_select'
            }),
            'tipo_animal_otro': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'placeholder': 'Especifique qué animal es',
                'id': 'tipo_animal_otro_input'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'type': 'date'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'rows': 3,
                'placeholder': 'Comentarios adicionales'
            })
        }

class SolicitudCirugiaForm(forms.ModelForm):
    class Meta:
        model = Cirugia
        fields = ['paciente', 'tipo_animal', 'tipo_animal_otro', 'tipo_cirugia', 'fecha', 'quirofano']
        widgets = {
            'paciente': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'placeholder': 'Nombre de su mascota'
            }),
            'tipo_animal': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'id': 'tipo_animal_select'
            }),
            'tipo_animal_otro': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'placeholder': 'Especifique qué animal es',
                'id': 'tipo_animal_otro_input'
            }),
            'tipo_cirugia': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'placeholder': 'Ej: Esterilización, Cesárea'
            }),
            'fecha': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'type': 'datetime-local'
            }),
            'quirofano': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500'
            })
        }

class SolicitudUrgenciaForm(forms.ModelForm):
    class Meta:
        model = Urgencia
        fields = ['paciente', 'tipo_animal', 'tipo_animal_otro', 'prioridad', 'descripcion']
        widgets = {
            'paciente': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'placeholder': 'Nombre de su mascota'
            }),
            'tipo_animal': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'id': 'tipo_animal_select'
            }),
            'tipo_animal_otro': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'placeholder': 'Especifique qué animal es',
                'id': 'tipo_animal_otro_input'
            }),
            'prioridad': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-cyan-500',
                'rows': 4,
                'placeholder': 'Describa la emergencia en detalle'
            })
        }
