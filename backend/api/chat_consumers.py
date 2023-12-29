import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import EmptyPage, Paginator
from rest_framework.exceptions import APIException

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

        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group = f'chat_{self.chat_id}'

        user = self.scope['user']
        chat = Chat.objects.get(id=int(self.chat_id))

        if chat.initiator == user or chat.receiver == user:
            async_to_sync(self.channel_layer.group_add)(
                self.chat_group, self.channel_name
            )
            self.accept()

            messages = Message.objects.filter(chat=chat).order_by('-pub_date')
            paginator = Paginator(messages, settings.MESSAGES_PAGE_SIZE)

            for message in reversed(paginator.page(1)):
                serializer = MessageSerializer(instance=message)
                self.send(text_data=json.dumps(
                    serializer.data,
                    ensure_ascii=False
                ))
        else:
            self.close()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        chat = Chat.objects.get(id=int(self.chat_id))
        self.sender = self.scope['user']

        if 'action' in text_data_json:
            action = text_data_json['action']

            if action == 'load_more':
                page_number = text_data_json['page_number']
                messages = Message.objects.filter(
                    chat=chat,
                ).order_by('-pub_date')
                paginator = Paginator(messages, settings.MESSAGES_PAGE_SIZE)

                try:
                    page = reversed(paginator.page(page_number))
                except EmptyPage:
                    self.send(text_data='Нет более ранних сообщений')
                    return

                for message in page:
                    serializer = MessageSerializer(instance=message)
                    self.send(text_data=json.dumps(
                        serializer.data,
                        ensure_ascii=False
                    ))

        else:
            message = text_data_json['message']

            if 'file' in text_data_json:
                try:
                    file = text_data_json['file']
                    if isinstance(file, bytes):
                        content_file = ContentFile(file)
                    else:
                        content = file.read()
                        content_file = ContentFile(content)

                    if content_file.size > settings.MAX_FILE_SIZE:
                        raise APIException('Слишком большой размер файла')
                    file_path = default_storage.save(
                        'messages/' + file.name,
                        content_file
                    )

                    message_create = Message.objects.create(
                        sender=self.sender,
                        text=message,
                        chat=chat,
                        file=file_path,
                    )
                    self.message_id = message_create.id

                    async_to_sync(self.channel_layer.group_send)(
                        self.chat_group,
                        {
                            'type': 'chat_message',
                            'message': message,
                            'file': file_path.url
                        }
                    )
                except AttributeError:
                    raise APIException('Неверный формат файла')

            else:
                message_create = Message.objects.create(
                    sender=self.sender,
                    text=message,
                    chat=chat,
                )
                self.message_id = message_create.id

                async_to_sync(self.channel_layer.group_send)(
                    self.chat_group,
                    {'type': 'chat_message', 'message': message}
                )

    def chat_message(self, event):
        if self.message_id:
            message = Message.objects.filter(id=self.message_id)
            serializer = MessageSerializer(instance=message[0])

            self.send(text_data=json.dumps(
                serializer.data,
                ensure_ascii=False
            ))

            self.sender = None
            self.message_id = None

        else:
            chat = Chat.objects.get(id=int(self.chat_id))
            last_message = Message.objects.filter(
                chat=chat,
            ).order_by('-pub_date').first()

            if last_message:
                serializer = MessageSerializer(instance=last_message)
                self.send(text_data=json.dumps(
                    serializer.data,
                    ensure_ascii=False
                ))
