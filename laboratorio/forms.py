# Formularios para análisis de laboratorio
from django import forms
from .models import Analisis

class AnalisisForm(forms.ModelForm):
    class Meta:
        model = Analisis
        fields = ['nombre', 'paciente', 'fecha', 'hora', 'resultado', 'notas', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        if fecha and hora:
            import datetime
            from consultas.utils import fecha_hora_disponible
            fecha_dt = datetime.datetime.combine(fecha, hora)
            exclude_id = self.instance.id if self.instance and self.instance.pk else None
            if not fecha_hora_disponible(fecha_dt, exclude_model='Analisis', exclude_id=exclude_id):
                self.add_error('fecha', 'Esta fecha y hora ya están reservadas por otro usuario. Por favor, elige otro horario disponible.')
        return cleaned_data
