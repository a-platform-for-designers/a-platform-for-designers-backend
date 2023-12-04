import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from api.serializers.message_serializers import MessageSerializer
from job.models import Chat, Message


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.sender = None
        self.message_id = None

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
        chat = Chat.objects.get(id=int(self.room_name))
        self.sender = self.scope["user"]     

        message_create = Message.objects.create(
                sender=self.sender,
                text=message,
                chat=chat,
        )
        self.message_id = message_create.id

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        # message = event["message"]
        # sender = self.scope["user"]
        if self.message_id:
            print("sender")
            message = Message.objects.filter(id=self.message_id)
            serializer = MessageSerializer(instance=message[0])

            self.send(text_data=json.dumps(serializer.data))
            self.sender = None
            self.message_id = None

        else:
            print("receiver")
            chat = Chat.objects.get(id=int(self.room_name))
            # Получаем последнее сообщение и отправляем его на отображение
            last_message = Message.objects.filter(chat=chat).order_by('-pub_date').first()
            if last_message:
                serializer = MessageSerializer(instance=last_message)
                self.send(text_data=json.dumps(serializer.data))
