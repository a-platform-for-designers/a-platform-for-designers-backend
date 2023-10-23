from django.db import models

class Resume(models.Model):
    user = models.ForeignKey(
        'User',
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


class Resource(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'

    def __str__(self):
        return self.name


class Contact(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='resume'
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE
    )
    reference = models.CharField(max_length=50)
    is_preference =  models.BooleanField()

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакт'

    def __str__(self):
        return f'Контакт {self.name}'