from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs


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
        # Извлекаем параметры строки запроса из scope
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_params = parse_qs(query_string)

        # Проверяем, есть ли токен среди параметров строки запроса
        token_key = query_params.get("token")
        if token_key:
            # Извлекаем первый токен из списка параметров
            token = token_key[0]
            # Получаем пользователя по токену и обновляем scope
            scope["user"] = await get_user(token)
        else:
            # Если токен не найден, устанавливаем AnonymousUser
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)
