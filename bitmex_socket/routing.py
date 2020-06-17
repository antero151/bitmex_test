from channels.routing import URLRouter
from django.urls import path

from . import consumers

websockets = URLRouter([
    path('ws/bitmex/', consumers.BitmexConsumer),
])
