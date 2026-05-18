# Formularios para consultas veterinarias
from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    # Formulario para crear y editar consultas veterinarias
    class Meta:
        model = Consulta
        fields = ['mascota', 'paciente', 'veterinario', 'fecha', 'motivo', 'diagnostico', 'estado']
        
        widgets = {
            'mascota': forms.Select(attrs={'class': 'w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 outline-none transition-all bg-white'}),
            'paciente': forms.TextInput(attrs={'class': 'w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 outline-none transition-all', 'placeholder': 'Escribe el nombre si no está en la lista anterior'}),
            'veterinario': forms.Select(attrs={'class': 'w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 outline-none transition-all bg-white'}),
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 outline-none transition-all bg-white'}),
            'motivo': forms.Textarea(attrs={'class': 'w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 outline-none transition-all', 'rows': 3, 'placeholder': 'Describe los síntomas o el motivo de la cita...'}),
            'diagnostico': forms.Textarea(attrs={'class': 'w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 outline-none transition-all', 'rows': 3, 'placeholder': 'Diagnóstico clínico (solo veterinarios)...'}),
            'estado': forms.Select(attrs={'class': 'w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 outline-none transition-all bg-white'}),
        }
        labels = {
            'mascota': 'Selecciona tu Mascota',
            'paciente': 'O nombre del Paciente (si es nuevo)',
            'veterinario': 'Veterinario de preferencia',
            'fecha': 'Fecha y Hora de la cita',
            'motivo': 'Motivo de la consulta',
            'diagnostico': 'Diagnóstico Veterinario',
            'estado': 'Estado de la cita'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['paciente'].required = False
        self.fields['mascota'].required = False

        if user:
            from mascotas.models import Mascota
            es_empleado = user.is_staff or user.is_superuser
            if hasattr(user, 'perfil') and user.perfil.rol in ['recepcionista', 'admin', 'veterinario', 'auxiliar']:
                es_empleado = True

            if not es_empleado:
                # Si es cliente, solo ve sus mascotas y no ve diagnostico ni estado
                self.fields['mascota'].queryset = Mascota.objects.filter(dueno=user)
                if 'diagnostico' in self.fields:
                    del self.fields['diagnostico']
                if 'estado' in self.fields:
                    del self.fields['estado']
            else:
                self.fields['mascota'].queryset = Mascota.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        mascota = cleaned_data.get('mascota')
        paciente = cleaned_data.get('paciente')
        fecha = cleaned_data.get('fecha')
        
        if mascota and not paciente:
            cleaned_data['paciente'] = mascota.nombre
        elif not mascota and not paciente:
            self.add_error('mascota', 'Debes seleccionar una mascota o escribir el nombre del paciente.')
            self.add_error('paciente', 'Debes seleccionar una mascota o escribir el nombre del paciente.')
            
        if fecha:
            from consultas.utils import fecha_hora_disponible
            exclude_id = self.instance.id if self.instance and self.instance.pk else None
            if not fecha_hora_disponible(fecha, exclude_model='Consulta', exclude_id=exclude_id):
                self.add_error('fecha', 'Esta fecha y hora ya están reservadas por otro usuario. Por favor, elige otro horario disponible.')
            
        return cleaned_data
