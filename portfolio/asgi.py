# portfolio/asgi.py

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import portfolio.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_portfolio.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            portfolio.routing.websocket_urlpatterns
        )
    ),
})