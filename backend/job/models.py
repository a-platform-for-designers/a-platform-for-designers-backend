from django.conf import settings
from django.db import models
from django.db.models.constraints import UniqueConstraint

from users.models import User


class Chat(models.Model):
    """Модель чата."""

    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chats_initiator',
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chats_receiver',
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        constraints = [
            UniqueConstraint(
                fields=['initiator', 'receiver'],
                name='unique_initiator_receiver'
            ),
        ]

    def __str__(self):
        return f'{self.initiator.email} - {self.receiver.email}'


class Message(models.Model):
    """Модель сообщения чата."""

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message_sender',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.sender.email}: {self.text[:settings.MESSAGE_STR]}'
