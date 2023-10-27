from django.db import models
from users.models import User

class Resume(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resume'
    )
    skills = models.ForeignKey('Skill', on_delete=models.SET_NULL, null=True)
    instruments = models.ForeignKey(
        'Instrument',
        on_delete=models.SET_NULL,
        null=True
    )
    about = models.TextField()
    status = instruments

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'

    def __str__(self):
        return f'Резюме {self.user.username}'


class Specialization(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.name


class Like(models.Model):
    liker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likers'
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'{self.liker} лайкнул {self.author}'


class Level_language(models.Model):
    speaker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='languages'
    )
    language = models.CharField(max_length=20)
    level = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        return f'{self.speaker} владеет {self.language}'


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    title = models.CharField(max_length=150)
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        null=True
    )
    price_min = models.PositiveIntegerField(blank=True, null=True)
    price_max = models.PositiveIntegerField(blank=True, null=True)
    currency = models.CharField(max_length=20)
    sphere = models.ForeignKey('Sphere', on_delete=models.SET_NULL, null=True)
    skills = models.ForeignKey('Skill', on_delete=models.SET_NULL, null=True)
    instruments = models.ForeignKey(
        'Instrument',
        on_delete=models.SET_NULL,
        null=True
    )
    description = models.TextField()

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'

    def __str__(self):
        return f'Резюме {self.user.username}'