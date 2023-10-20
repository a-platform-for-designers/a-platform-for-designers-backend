from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

MIN_AMOUNT = 1
MAX_AMOUNT = 32000


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

    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    status = models.CharField(
        max_length=200,
        verbose_name='Статус проекта'
    )

    sphere = models.CharField(
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

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['title']

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