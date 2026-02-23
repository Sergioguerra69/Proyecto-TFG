# Consumer para WebSockets - Sistema de notificaciones
# Permite que los usuarios reciban mensajes en tiempo real

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacionConsumer(AsyncWebsocketConsumer):
    # Maneja las conexiones WebSocket para notificaciones
    
    async def connect(self):
        # Cuando un usuario se conecta
        self.room_group_name = 'clinica_notificaciones'
        
        # Añadimos al usuario al grupo de notificaciones
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Aceptamos la conexión
        await self.accept()
        
        # Enviamos mensaje de bienvenida
        await self.send(text_data=json.dumps({
            'message': '¡Conectado al sistema de notificaciones de VetCT!'
        }))

    async def disconnect(self, close_code):
        # Cuando un usuario se desconecta
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Cuando recibimos un mensaje del cliente
        try:
            # Intentamos leer como JSON
            data = json.loads(text_data)
            mensaje = data.get('message', text_data)
        except:
            # Si no es JSON, usamos el texto directamente
            mensaje = text_data

        # Respondemos al cliente
        await self.send(text_data=json.dumps({
            'message': f'Mensaje recibido: {mensaje}'
        }))
        
    # Esta función recibe los mensajes que se envían al grupo
    async def enviar_notificacion(self, event):
        message = event['message']
        
        # Enviamos el mensaje a todos los usuarios conectados
        await self.send(text_data=json.dumps({
            'message': message
        }))
