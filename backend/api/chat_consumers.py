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
            self.close()

        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_group = f"chat_{self.chat_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group, self.channel_name
        )
        self.accept()

        chat = Chat.objects.get(id=int(self.chat_id))
        messages = Message.objects.filter(chat=chat).order_by('pub_date')

        for message in messages:
            serializer = MessageSerializer(instance=message)
            self.send(text_data=json.dumps(serializer.data))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        chat = Chat.objects.get(id=int(self.chat_id))
        self.sender = self.scope["user"]

        message_create = Message.objects.create(
            sender=self.sender,
            text=message,
            chat=chat,
        )
        self.message_id = message_create.id

        async_to_sync(self.channel_layer.group_send)(
            self.chat_group,
            {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):
        if self.message_id:
            message = Message.objects.filter(id=self.message_id)
            serializer = MessageSerializer(instance=message[0])

            self.send(text_data=json.dumps(serializer.data))

            self.sender = None
            self.message_id = None

        else:
            chat = Chat.objects.get(id=int(self.chat_id))
            last_message = Message.objects.filter(
                chat=chat,
            ).order_by('-pub_date').first()

            if last_message:
                serializer = MessageSerializer(instance=last_message)
                self.send(text_data=json.dumps(serializer.data))
