from django.conf import settings
from django.db import models
from django.db.models.constraints import UniqueConstraint
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


MIN_AMOUNT = 1
MAX_AMOUNT = 1000


class Instrument(models.Model):
    """Модель инструментов."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'
        ordering = ['name',]

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    """Модель навыков."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['name',]

    def __str__(self) -> str:
        return self.name


class Case(models.Model):
    """Модель проекта."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='case',
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    sphere = models.CharField(
        max_length=200,
        verbose_name='Сфера'
    )

    instruments = models.ManyToManyField(
        Instrument,
        verbose_name='Список инструментов'
    )

    skills = models.ManyToManyField(
        Skill,
        verbose_name='Список навыков'
    )

    working_term = models.PositiveSmallIntegerField(
        verbose_name='Время изготовления (в часах)',
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message='Время изготовления не менее 1 часа'),
            MaxValueValidator(
                MAX_AMOUNT,
                message='Время изготовления не может быть бесконечным'
            )
        ]
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.title


class Favorite(models.Model):
    """Модель избранных проектов."""

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='is_favorited',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',

    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['case']

    def __str__(self):
        return (f'Пользователь {self.user} добавил {self.case} '
                'в избранное')


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


# заглушка
class Order(models.Model):
    pass


class CaseImage(models.Model):
    """Модель изображения для кейса."""

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='image_in_case',
    )
    is_avatar = models.BooleanField()
    picture = models.ImageField()
    name = models.CharField(
        max_length=50,
        verbose_name='Название изображения'
    )
    description = models.TextField(
        max_length=300,
    )

    class Meta:
        verbose_name = 'Изображение кейса'
        verbose_name_plural = 'Изображения кейса'

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    """Модель комментария."""

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
    )   
    comment_text = models.TextField(
        max_length=300,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.name


class FavoriteOrder(models.Model):
    """Модель избранного заказа."""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_order',
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='favorite_order',
    )

    class Meta:
        verbose_name = 'Избранный заказ'
        verbose_name_plural = 'Избранные заказ'

    def __str__(self) -> str:
        return self.name


class Sphere(models.Model):
    """Модель сферы деятельности"""

    name = models.CharField(
        max_length=200,
        verbose_name='Название деятельности'
    )

    class Meta:
        verbose_name = 'Сфера деятельности'
        verbose_name_plural = 'Сферы деятельности'
        ordering = ['name',]

    def __str__(self) -> str:
        return self.name
