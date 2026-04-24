"""
ASGI config for vetct_web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
import notificaciones.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetct_web.settings')

# Middleware simple que no causa problemas de autenticación
class SimpleMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        return await self.inner(scope, receive, send)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": SimpleMiddleware(
        URLRouter(
            notificaciones.routing.websocket_urlpatterns
        )
    ),
})
