import django  # noqa: E402
from django.core.asgi import get_asgi_application  # noqa: E402

django.setup()

from channels.routing import URLRouter, ProtocolTypeRouter  # noqa: E402
from channels.security.websocket import (  # noqa: E402
    AllowedHostsOriginValidator
)
from .tokenauth_middleware import TokenAuthMiddleware  # noqa: E402
from api import chat_routing  # noqa: E402

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(chat_routing.websocket_urlpatterns)
        )
    )
})
