from rest_framework import serializers

from support.models import SupportTicket


class SupportTicketSerializer(serializers.ModelSerializer):
    """
    Сериализатор для сообщения в поддержку.

    """
    message = serializers.CharField(max_length=1500)

    class Meta:
        model = SupportTicket
        fields = [
            'name',
            'email',
            'subject',
            'message'
        ]
