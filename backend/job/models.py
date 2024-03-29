from django.conf import settings
# from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

from users.models import User


class Instrument(models.Model):
    """
    Модель инструментов

    """

    name = models.CharField(
        max_length=40,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'
        ordering = ['name',]

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    """
    Модель навыков

    """

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


class Sphere(models.Model):
    """
    Модель сферы деятельности

    """

    name = models.CharField(
        max_length=60,
        verbose_name='Название деятельности'
    )

    class Meta:
        verbose_name = 'Сфера деятельности'
        verbose_name_plural = 'Сферы деятельности'
        ordering = ['name',]

    def __str__(self) -> str:
        return self.name


class Specialization(models.Model):
    """
    Модель специализации

    """
    name = models.CharField(
        max_length=25,
        verbose_name='Название специализации'
    )

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
        ordering = ['name',]

    def __str__(self) -> str:
        return self.name


class Language(models.Model):
    """
    Модель языка

    """
    name = models.CharField(
        max_length=56,
        verbose_name='Язык'
    )

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'
        ordering = ['name',]

    def __str__(self) -> str:
        return self.name


class Case(models.Model):
    """
    Модель проекта

    """

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='case',
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Название'
    )

    avatar = models.ImageField()
    specialization = models.ForeignKey(
        Specialization,
        verbose_name='Специализация',
        on_delete=models.SET_NULL,
        related_name='specialization',
        blank=True,
        null=True
    )

    sphere = models.ForeignKey(
        Sphere,
        verbose_name='Сфера',
        on_delete=models.SET_NULL,
        related_name='sphere',
        blank=True,
        null=True
    )

    instruments = models.ManyToManyField(
        Instrument,
        verbose_name='Список инструментов',
        blank=True,
    )

    working_term = models.CharField(
        verbose_name='Время, затраченное на изготовление проекта',
        max_length=50,
        blank=True,
        null=True
    )

    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
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


class FavoriteCase(models.Model):
    """
    Модель избранных проектов

    """

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='favorite_cases',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_cases',

    )

    class Meta:
        verbose_name = 'Избранный проекты'
        verbose_name_plural = 'Избранные проекты'
        ordering = ['case']

    def __str__(self):
        return (f'Пользователь {self.user} добавил {self.case} '
                'в избранный проект')


class Chat(models.Model):
    """
    Модель чата

    """

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
        ordering = ['-id']
        constraints = [
            UniqueConstraint(
                fields=['initiator', 'receiver'],
                name='unique_initiator_receiver'
            ),
        ]

    def __str__(self):
        return f'{self.initiator.email} - {self.receiver.email}'


class Message(models.Model):
    """
    Модель сообщения чата

    """

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
    file = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.sender.email}: {self.text[:settings.MESSAGE_STR]}'


class File(models.Model):
    """
    Модель файлов из сообщений

    """
    file = models.FileField(upload_to='messages/')
    pub_date = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='files',
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='file_sender',
    )

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.file}'


class CaseImage(models.Model):
    """
    Модель изображения для кейса

    """
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField()

    class Meta:
        verbose_name = 'Изображение кейса'
        verbose_name_plural = 'Изображения кейса'

    def __str__(self):
        return "%s" % (self.case.title)


# class Comment(models.Model):
#     """
#     Модель комментария

#     """

#     case = models.ForeignKey(
#         Case,
#         on_delete=models.CASCADE,
#         related_name='comment',
#     )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         related_name='comment',
#         null=True
#     )
#     comment_text = models.TextField(
#         max_length=300,
#     )

#     class Meta:
#         verbose_name = 'Комментарий'
#         verbose_name_plural = 'Комментарии'

#     def __str__(self) -> str:
#         return self.name


class Mentoring(models.Model):
    """
    Модель менторства

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=200)
    expertise = models.TextField(validators=[
        MaxLengthValidator(500, 'Поле должно содержать не более 500 символов')
    ])
    price = models.PositiveIntegerField(null=True, blank=True)
    agreement_free = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = 'Менторство'

    def __str__(self):
        return f'Менторство {self.user.email}'


class Like(models.Model):
    """Модель лайков."""

    liker = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='likes',
        null=True
    )
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='case_likes'
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'{self.liker} лайкнул {self.case}'


class Order(models.Model):
    """
    Модель заказа

    """

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    # executor = models.ForeignKey(
    #     User,
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name='executed_orders'
    # )
    title = models.CharField(max_length=150)
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        null=True
    )
    payment = models.PositiveIntegerField(blank=True, null=True)
    sphere = models.ForeignKey(Sphere, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.title} '


class OrderResponse(models.Model):
    """
    Общая модель для отклика на заказ и избранного заказа

    """

    user = user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='order_responses',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_responses',
    )

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


class FavoriteOrder(models.Model):
    """
    Модель избранного заказа

    """

    user = user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_orders',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='favorite_orders',
    )

    class Meta:
        verbose_name = 'Избранный заказ'
        verbose_name_plural = 'Избранные заказы'
