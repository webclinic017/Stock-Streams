# chat/routing.py
from django.urls import re_path

from . import consumer

# print("using portfolio routing")

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumer.ChatConsumer.as_asgi()),
    re_path(r'ws/stream/(?P<symbol>\w+)/$', consumer.AlpacaConsumer.as_asgi()),
]

# channel_routing = {}

