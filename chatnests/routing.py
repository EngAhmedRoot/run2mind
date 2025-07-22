from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # تحديد المسار للـ WebSocket مع الاستبدال بالـ room_name
    re_path(r'ws/chat/(?P<room_name>chat_\d+_\d+)/$', consumers.ChatConsumer.as_asgi()),
]
