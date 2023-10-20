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