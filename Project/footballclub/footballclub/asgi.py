import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from footballclub import routing  # Import your WebSocket routing configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'footballclub.settings')

# Define the WebSocket protocol routing and use AuthMiddlewareStack
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
