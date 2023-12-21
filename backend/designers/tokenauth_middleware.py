from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = scope.get("headers", [])
        for name, value in headers:
            if name.decode("utf-8") == "cookie":
                token = next((
                    v.split("=")[1] for v in value.decode(
                        "utf-8"
                    ).split("; ") if v.startswith("token=")
                ), None)
                if token:
                    scope["user"] = await get_user(token)
        return await self.inner(scope, receive, send)
