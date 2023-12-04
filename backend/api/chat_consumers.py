import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from users.models import User
from job.models import Chat, Message
from api.serializers.message_serializers import MessageSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        if 'user' not in self.scope:
            # Если пользователь не авторизован, закрываем соединение
            self.close()
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        # Получаем все сообщения из чата
        chat = Chat.objects.get(id=int(self.room_name))
        messages = Message.objects.filter(chat=chat).order_by('pub_date')

        # Отправляем все сообщения пользователю
        for message in messages:
            serializer = MessageSerializer(instance=message)
            self.send(text_data=json.dumps(serializer.data))


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        chat = Chat.objects.get(id=int(self.room_name))
        sender = self.scope['user']

        message = Message.objects.create(
            sender=sender,
            text=message,
            chat=chat,
        )
        serializer = MessageSerializer(instance=message)
        # Send message to WebSocket
        self.send(text_data=json.dumps(serializer.data))
