from channels.routing import ProtocolTypeRouter, ChannelNameRouter

from bitmex_socket.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})
