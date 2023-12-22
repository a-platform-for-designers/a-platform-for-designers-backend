from channels.routing import URLRouter, ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from .tokenauth_middleware import TokenAuthMiddleware
from api import chat_routing


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(URLRouter(chat_routing.websocket_urlpatterns))
    )
})
