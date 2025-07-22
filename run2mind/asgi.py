import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chatnests.routing import websocket_urlpatterns

# تحديد إعدادات المشروع
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'run2mind.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # ربط مسارات WebSocket من `routing.py`
        )
    ),
})
