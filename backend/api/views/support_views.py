import requests
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema

from api.serializers.support_serializers import SupportTicketSerializer


class SupportTicketView(APIView):
    """
    Вью для создания и отправки сообщения в поддержку.

    """
    http_method_names = ['post']
    permission_classes = [AllowAny]

    @extend_schema(
        request=SupportTicketSerializer,
        responses={201: SupportTicketSerializer},
        summary="Создать обращение в поддержку",
        description="Позволяет пользователям создавать "
        "обращение в службу поддержки."
    )
    def post(self, request, *args, **kwargs):
        serializer = SupportTicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket = serializer.save()
            self.send_telegram_notification(ticket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_telegram_notification(self, ticket):
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        text = f"Новое обращение от {ticket.name}: {ticket.subject}"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {'chat_id': chat_id, 'text': text}
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"Ошибка при отправке уведомления в Telegram: {e}")
