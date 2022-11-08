"""
ASGI config for facebook project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from core.consumer import *
from interact.consumer import *
from user.consumer import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook.settings')

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AuthMiddlewareStack(
        URLRouter([
            path("interact/", UserInteractConsumer.as_asgi()),
            path("noti/", NotiConsumer.as_asgi()),
            path("friend/", FriendConsumer.as_asgi()),
            path("chat/", ChatConsumer.as_asgi()),
        ])
    ),
})

