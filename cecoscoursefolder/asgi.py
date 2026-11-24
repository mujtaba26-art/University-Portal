import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cecoscoursefolder.settings')

django_asgi_app = get_asgi_application() 

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # 👈 This line is required
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns,
        )
    ),
})
