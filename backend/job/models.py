from django.db import models
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


# заглушка
class Case(models.Model):
    pass


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