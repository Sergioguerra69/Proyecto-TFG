from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from consultas.models import Consulta
from vacunacion.models import Vacuna
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Envía recordatorios automáticos de citas y vacunas por correo electrónico'

    def handle(self, *args, **kwargs):
        hoy = timezone.now().date()
        manana = hoy + timedelta(days=1)
        semana_que_viene = hoy + timedelta(days=7)

        # sacar las citas de manana que esten pendientes o aceptadas
        citas_manana = Consulta.objects.filter(
            fecha__date=manana,
            estado__in=['Pendiente', 'Aceptada']
        )
        
        citas_enviadas = 0
        for cita in citas_manana:
            if cita.correo or (cita.usuario and cita.usuario.email):
                email_dest = cita.correo if cita.correo else cita.usuario.email
                nombre_paciente = cita.mascota.nombre if cita.mascota else cita.paciente
                hora_str = cita.fecha.strftime("%H:%M")
                
                asunto = f"Recordatorio: Cita veterinaria para {nombre_paciente} mañana a las {hora_str}"
                mensaje = f"Hola,\n\nTe recordamos que tienes una cita programada para {nombre_paciente} mañana a las {hora_str}.\n\nMotivo: {cita.motivo}\n\nPor favor, si no puedes asistir, contáctanos para cancelar o reprogramar.\n\nAtentamente,\nClínica Veterinaria VetCT"
                
                try:
                    send_mail(
                        asunto,
                        mensaje,
                        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@vetct.com',
                        [email_dest],
                        fail_silently=True,
                    )
                    citas_enviadas += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error enviando email a {email_dest}: {str(e)}'))

        # avisos de vacunas que tocan la proxima semana
        vacunas_proximas = Vacuna.objects.filter(
            proxima_dosis=semana_que_viene
        )
        
        vacunas_enviadas = 0
        for vacuna in vacunas_proximas:
            if vacuna.mascota.dueno.email:
                email_dest = vacuna.mascota.dueno.email
                nombre_paciente = vacuna.mascota.nombre
                
                asunto = f"Aviso de Vacunación: A {nombre_paciente} le toca la vacuna la próxima semana"
                mensaje = f"Hola {vacuna.mascota.dueno.username},\n\nTe informamos de que a {nombre_paciente} le corresponde la vacuna '{vacuna.nombre}' la semana que viene ({semana_que_viene.strftime('%d/%m/%Y')}).\n\nPor favor, pide cita lo antes posible.\n\nAtentamente,\nClínica Veterinaria VetCT"
                
                try:
                    send_mail(
                        asunto,
                        mensaje,
                        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@vetct.com',
                        [email_dest],
                        fail_silently=True,
                    )
                    vacunas_enviadas += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error enviando email a {email_dest}: {str(e)}'))
                    
        self.stdout.write(self.style.SUCCESS(f'Proceso completado. Recordatorios de citas: {citas_enviadas}. Recordatorios de vacunas: {vacunas_enviadas}.'))
