"""
ASGI config for vetct_web project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notificaciones.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetct_web.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notificaciones.routing.websocket_urlpatterns
        )
    ),
})
