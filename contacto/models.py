# Modelos para el sistema de contacto
from django.db import models
from django.contrib.auth.models import User

# Modelo para formularios de contacto
class FormularioContacto(models.Model):
    # Estados posibles del formulario
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Respondido', 'Respondido'),
        ('Cerrado', 'Cerrado'),
    ]
    
    # Información del solicitante
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellidos = models.CharField(max_length=100, blank=True, verbose_name='Apellidos')
    dni = models.CharField(max_length=20, verbose_name='DNI')
    email = models.EmailField(verbose_name='Correo electrónico')
    telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    
    # Contenido del mensaje
    asunto = models.CharField(max_length=200, verbose_name='Asunto')
    mensaje = models.TextField(verbose_name='Mensaje')
    
    # Información de la solicitud
    fecha = models.DateField(null=True, blank=True, verbose_name='Fecha preferida')
    hora = models.TimeField(null=True, blank=True, verbose_name='Hora preferida')
    
    # Control del sistema
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    # Quién respondió (cuando se responde)
    respondido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='formularios_respondidos', verbose_name='Respondido por')
    fecha_respuesta = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de respuesta')

    class Meta:
        verbose_name = "Formulario de contacto"
        verbose_name_plural = "Formularios de contacto"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - {self.asunto} ({self.fecha_creacion.date()})"

# Modelo para respuestas a formularios de contacto
class RespuestaContacto(models.Model):
    # Relación con el formulario original
    formulario = models.ForeignKey(FormularioContacto, on_delete=models.CASCADE, 
                              related_name='respuestas', verbose_name='Formulario')
    
    # Quién responde
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    
    # Contenido de la respuesta
    contenido = models.TextField(verbose_name='Respuesta')
    
    # Control temporal
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de respuesta')

    class Meta:
        verbose_name = "Respuesta de contacto"
        verbose_name_plural = "Respuestas de contacto"
        ordering = ['fecha_creacion']

    def __str__(self):
        return f"Respuesta de {self.autor.username} a {self.formulario.nombre}"

# Modelo para mensajes de clientes (dudas, chat)
class MensajeCliente(models.Model):
    # Estados posibles del mensaje
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Leído', 'Leído'),
        ('Respondido', 'Respondido'),
        ('Cerrado', 'Cerrado'),
    ]
    
    # Información del cliente
    nombre = models.CharField(max_length=100, verbose_name='Nombre completo')
    email = models.EmailField(verbose_name='Correo electrónico')
    telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    
    # Contenido del mensaje
    asunto = models.CharField(max_length=200, verbose_name='Asunto')
    mensaje = models.TextField(verbose_name='Mensaje')
    
    # Control del sistema
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    # Quién respondió (cuando se responde)
    respondido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='mensajes_respondidos', verbose_name='Respondido por')
    fecha_respuesta = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de respuesta')

    class Meta:
        verbose_name = "Mensaje de cliente"
        verbose_name_plural = "Mensajes de clientes"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - {self.asunto} ({self.fecha_creacion.date()})"

# Modelo para respuestas a mensajes de clientes (chat)
class RespuestaMensaje(models.Model):
    # Relación con el mensaje original
    mensaje = models.ForeignKey(MensajeCliente, on_delete=models.CASCADE, 
                              related_name='respuestas_chat', verbose_name='Mensaje')
    
    # Quién responde (recepcionista o cliente)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    es_cliente = models.BooleanField(default=False, verbose_name='Es respuesta del cliente')
    
    # Contenido de la respuesta
    contenido = models.TextField(verbose_name='Respuesta')
    
    # Control temporal
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de respuesta')

    class Meta:
        verbose_name = "Respuesta al mensaje"
        verbose_name_plural = "Respuestas a mensajes"
        ordering = ['fecha_creacion']

    def __str__(self):
        autor_tipo = "Cliente" if self.es_cliente else "Recepcionista"
        return f"Respuesta de {autor_tipo} a {self.mensaje.nombre}"

# Modelo para asignación de solicitudes a veterinarios
class AsignacionSolicitud(models.Model):
    # Estados posibles de la asignación
    ESTADO_CHOICES = [
        ('Asignada', 'Asignada'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
        ('Completada', 'Completada'),
    ]
    
    # Relación con el formulario de contacto original
    formulario = models.ForeignKey(FormularioContacto, on_delete=models.CASCADE, 
                                  related_name='asignaciones', verbose_name='Formulario de contacto')
    
    # Veterinario asignado
    veterinario = models.ForeignKey(User, on_delete=models.CASCADE, 
                                    related_name='solicitudes_asignadas', verbose_name='Veterinario')
    
    # Quién hizo la asignación (recepcionista)
    asignado_por = models.ForeignKey(User, on_delete=models.CASCADE, 
                                     related_name='asignaciones_realizadas', verbose_name='Asignado por')
    
    # Estado de la asignación
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Asignada')
    
    # Fechas importantes
    fecha_asignacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')
    fecha_aceptacion = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de aceptación')
    fecha_completacion = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de completación')
    
    # Notas adicionales
    notas_asignacion = models.TextField(blank=True, verbose_name='Notas de asignación')
    notas_veterinario = models.TextField(blank=True, verbose_name='Notas del veterinario')

    class Meta:
        verbose_name = "Asignación de solicitud"
        verbose_name_plural = "Asignaciones de solicitudes"
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f"Solicitud de {self.formulario.nombre} asignada a {self.veterinario.username}"

# Modelo para notificaciones a veterinarios
class NotificacionVeterinario(models.Model):
    # Tipos de notificación
    TIPO_CHOICES = [
        ('asignacion', 'Nueva asignación'),
        ('aceptacion', 'Solicitud aceptada'),
        ('rechazo', 'Solicitud rechazada'),
        ('mensaje', 'Nuevo mensaje'),
    ]
    
    # Veterinario destinatario
    veterinario = models.ForeignKey(User, on_delete=models.CASCADE, 
                                    related_name='notificaciones', verbose_name='Veterinario')
    
    # Información de la notificación
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo de notificación')
    titulo = models.CharField(max_length=200, verbose_name='Título')
    mensaje = models.TextField(verbose_name='Mensaje')
    
    # Relación opcional con la asignación
    asignacion = models.ForeignKey(AsignacionSolicitud, on_delete=models.CASCADE, 
                                   null=True, blank=True, related_name='notificaciones', 
                                   verbose_name='Asignación relacionada')
    
    # Estado de la notificación
    leida = models.BooleanField(default=False, verbose_name='Leída')
    
    # Control temporal
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_lectura = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de lectura')

    class Meta:
        verbose_name = "Notificación veterinario"
        verbose_name_plural = "Notificaciones veterinarios"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Notificación {self.get_tipo_display()} para {self.veterinario.username}"
