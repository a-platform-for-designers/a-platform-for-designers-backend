from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

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


class Sphere(models.Model):
    """Модель сферы."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Сфера'
        verbose_name_plural = 'Сферы'
        ordering = ['name']


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

    sphere = models.ManyToManyField(
        Sphere,
        verbose_name='Сфера'
    )

    # images = models.ManyToManyField(
    #     CaseImage,
    #     verbose_name='Фотография',
    #     through='CaseImage'
    # )

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


class FavoriteCase(models.Model):
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
