# Consumer WebSocket simple para notificaciones
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
    async def disconnect(self, close_code):
        pass
        
    async def receive(self, text_data):
        # Recibir mensaje del cliente
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'message': f"Recibido: {data['message']}"
        }))
        
    async def enviar_notificacion(self, event):
        # Enviar notificación simple
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'tipo': event.get('tipo', 'general')
        }))
