import asyncio
import os

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.core.files.storage import default_storage
from django.test import Client, TransactionTestCase, TestCase
from rest_framework.authtoken.models import Token

from designers.asgi import application
from job.models import Chat, Message
from users.models import User


class FileTransferTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='user@user.ru',
            password='testpassword',
            is_customer=False
        )
        self.token = Token.objects.create(user=self.user)

        chat = Chat.objects.create(initiator=self.user, receiver=self.user)
        self.chat_id = chat.pk

        self.client.force_login(self.user)

    async def connect_to_websocket(self, communicator):
        connected, _ = await communicator.connect()
        return connected

    def test_file_transfer(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_file_transfer())

    async def _test_file_transfer(self):
        communicator = WebsocketCommunicator(
            application,
            f'ws/chats/{self.chat_id}/',
            headers=[('cookie', f'token={self.token.key.encode("utf-8")}')]
        )
        communicator.scope['user'] = self.user
        print(communicator)
        print(communicator.scope['user'])
        connected = await self.connect_to_websocket(communicator)

        file_path = default_storage.path('messages/Colors.png')
        with open(file_path, 'rb') as file:
            file_content = file.read().decode('latin-1')

        message = {
            'message': 'Test file transfer',
            'file': file_content,
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()

        last_message = Message.objects.filter(chat_id=self.chat_id).latest('pub_date')
        self.assertEqual(last_message.sender, self.user)
        self.assertEqual(last_message.text, 'Test file transfer')
        self.assertIsNotNone(last_message.file)

        # Clean up the test file
        os.remove(file_path)

        await communicator.disconnect()
