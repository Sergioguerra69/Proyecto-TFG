# Sistema de notificaciones de la clínica
from django.db import models
from django.contrib.auth.models import User

class Notificacion(models.Model):
    # Tipos de notificaciones
    TIPO_CHOICES = [
        ('consulta', 'Consulta'),
        ('analisis', 'Análisis'),
        ('cirugia', 'Cirugía'),
        ('urgencia', 'Urgencia'),
        ('formulario_contacto', 'Formulario de Contacto'),
        ('mensaje_contacto', 'Mensaje de Duda'),
    ]
    
    # Estados de una notificación
    ESTADO_NOTIFICACION = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    
    # Quien recibe el mensaje (recepcionista/admin)
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_recibidas')
    # Quien envía el mensaje (cliente)
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_enviadas')
    # Tipo de solicitud (consulta, análisis, etc.)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    # ID del objeto relacionado
    objeto_id = models.PositiveIntegerField()
    # Estado de la notificación
    estado = models.CharField(max_length=20, choices=ESTADO_NOTIFICACION, default='pendiente')
    # Mensaje adicional (opcional)
    mensaje = models.TextField(blank=True)
    # Fecha de creación (automática)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Notificación {self.get_tipo_display()} - {self.emisor.username}"
    
    def get_objeto(self):
        """Obtener el objeto relacionado con la notificación"""
        if self.tipo == 'consulta':
            try:
                from consultas.models import Consulta
                return Consulta.objects.get(id=self.objeto_id)
            except Consulta.DoesNotExist:
                return None
        elif self.tipo == 'analisis':
            try:
                from laboratorio.models import Analisis
                return Analisis.objects.get(id=self.objeto_id)
            except Analisis.DoesNotExist:
                return None
        elif self.tipo == 'cirugia':
            try:
                from cirugias.models import Cirugia
                return Cirugia.objects.get(id=self.objeto_id)
            except Cirugia.DoesNotExist:
                return None
        elif self.tipo == 'urgencia':
            try:
                from urgencias.models import Urgencia
                return Urgencia.objects.get(id=self.objeto_id)
            except Urgencia.DoesNotExist:
                return None
        elif self.tipo == 'formulario_contacto':
            try:
                from contacto.models import FormularioContacto
                return FormularioContacto.objects.get(id=self.objeto_id)
            except FormularioContacto.DoesNotExist:
                return None
        elif self.tipo == 'mensaje_contacto':
            try:
                from contacto.models import MensajeCliente
                return MensajeCliente.objects.get(id=self.objeto_id)
            except MensajeCliente.DoesNotExist:
                return None
        return None
