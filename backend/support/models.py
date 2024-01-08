from django.db import models


class SupportTicket(models.Model):
    """
    Создание сообщения в поддержку.

    """
    name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    email = models.EmailField(
        verbose_name="Электронная почта"
    )
    subject = models.CharField(
        max_length=200,
        verbose_name="Тема"
    )
    message = models.TextField(
        verbose_name="Сообщение"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Прочитано"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.subject} от {self.name}"

    class Meta:
        ordering = ['is_read', 'created_at']
        verbose_name = "Обращение в поддержку"
        verbose_name_plural = "Обращения в поддержку"
