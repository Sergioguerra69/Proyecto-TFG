# Formularios para cirugías
from django import forms
from .models import Cirugia

class CirugiaForm(forms.ModelForm):
    class Meta:
        model = Cirugia
        fields = ['paciente', 'tipo_cirugia', 'fecha', 'estado', 'quirofano']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        if fecha:
            from consultas.utils import fecha_hora_disponible
            exclude_id = self.instance.id if self.instance and self.instance.pk else None
            if not fecha_hora_disponible(fecha, exclude_model='Cirugia', exclude_id=exclude_id):
                self.add_error('fecha', 'Esta fecha y hora ya están reservadas por otro usuario. Por favor, elige otro horario disponible.')
        return cleaned_data
