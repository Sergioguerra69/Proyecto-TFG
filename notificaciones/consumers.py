import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class NotificacionConsumer(AsyncWebsocketConsumer):
    """
    Consumer WebSocket para notificaciones en tiempo real.
    Cada usuario se une a su grupo personal (user_<id>)
    y al grupo de su rol (recepcion / veterinarios).
    """

    async def connect(self):
        # Obtener el usuario desde el scope (requiere AuthMiddlewareStack)
        self.user = self.scope.get("user", None)

        if self.user is None or not self.user.is_authenticated:
            # Rechazar conexión si no está autenticado
            await self.close()
            return

        # Grupo personal del usuario
        self.personal_group = f"user_{self.user.id}"

        # Grupos de rol
        # Identificar grupos por rol de perfil
        rol = getattr(self.user, 'perfil', None).rol if hasattr(self.user, 'perfil') else None
        
        if rol == 'veterinario':
            await self.channel_layer.group_add("veterinarios", self.channel_name)
        
        if rol == 'recepcionista':
            await self.channel_layer.group_add("recepcion", self.channel_name)
        
        # También mantener grupos de Django por si acaso
        grupos_usuario = [g.name for g in self.user.groups.all()]
        for grupo in grupos_usuario:
            await self.channel_layer.group_add(grupo.lower(), self.channel_name)
        
        await self.channel_layer.group_add("clinica_notificaciones", self.channel_name)

        await self.accept()

        # Confirmar conexion
        await self.send(text_data=json.dumps({
            "tipo": "conexion_ok",
            "message": f"Conectado como {self.user.username}",
            "rol": rol,
        }))

    async def disconnect(self, close_code):
        if hasattr(self, "personal_group"):
            await self.channel_layer.group_discard(self.personal_group, self.channel_name)

    async def receive(self, text_data):
        # El cliente puede enviar ping para mantener la conexion viva
        try:
            data = json.loads(text_data)
            if data.get("tipo") == "ping":
                await self.send(text_data=json.dumps({"tipo": "pong"}))
        except Exception:
            pass

    # ---- Handlers de eventos del channel layer ----

    async def notificacion_nueva(self, event):
        """Enviado cuando se crea una notificacion nueva para veterinarios."""
        await self.send(text_data=json.dumps({
            "tipo": "notificacion_nueva",
            "tipo_cita": event.get("tipo_cita"),
            "paciente": event.get("paciente"),
            "detalle": event.get("detalle"),
            "fecha_cita": event.get("fecha_cita"),
            "objeto_id": event.get("objeto_id"),
            "message": event.get("message"),
        }))

    async def cita_actualizada(self, event):
        """Enviado cuando el veterinario acepta o rechaza una cita."""
        await self.send(text_data=json.dumps({
            "tipo": "cita_actualizada",
            "accion": event.get("accion"),   # 'aceptada' | 'rechazada' | 'cancelada'
            "tipo_cita": event.get("tipo_cita"),
            "paciente": event.get("paciente"),
            "objeto_id": event.get("objeto_id"),
            "message": event.get("message"),
        }))

    async def enviar_notificacion(self, event):
        """Handler generico de compatibilidad."""
        await self.send(text_data=json.dumps({
            "tipo": "general",
            "message": event.get("message", ""),
        }))

    @database_sync_to_async
    def get_grupos_usuario(self):
        return list(self.user.groups.values_list("name", flat=True))
