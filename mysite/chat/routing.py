from django.urls import path
from . import consumers

# Lista adresów URL WebSocket
websocket_urlpatterns = [
    # Ścieżka do konsumera czatu, który obsługuje połączenia WebSocket
    path('chat/', consumers.ChatConsumer.as_asgi()),
]