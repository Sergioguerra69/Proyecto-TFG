# Modelos para el sistema de notificaciones
from django.db import models
from django.contrib.auth.models import User

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('consulta', 'Consulta'),
        ('analisis', 'Análisis'),
        ('cirugia', 'Cirugía'),
        ('urgencia', 'Urgencia'),
    ]
    
    ESTADO_NOTIFICACION = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    
    # Usuario que recibe la notificación (recepcionista/admin)
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_recibidas')
    # Usuario que creó la solicitud (cliente)
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_enviadas')
    # Tipo de solicitud
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    # ID del objeto relacionado
    objeto_id = models.PositiveIntegerField()
    # Estado de la notificación
    estado = models.CharField(max_length=20, choices=ESTADO_NOTIFICACION, default='pendiente')
    # Mensaje opcional
    mensaje = models.TextField(blank=True)
    # Fecha de creación
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Notificación {self.get_tipo_display()} - {self.emisor.username}"
    
    def get_objeto(self):
        """Obtener el objeto relacionado"""
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
        return None
