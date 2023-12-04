from django.urls import re_path

from . import chat_consumers


websocket_urlpatterns = [
    re_path(
        r"ws/chats/(?P<chat_id>\w+)/$",
        chat_consumers.ChatConsumer.as_asgi()
    ),
]
