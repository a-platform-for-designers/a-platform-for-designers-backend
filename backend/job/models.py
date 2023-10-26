from django.db import models
from users.models import User


# поставила просто заглушки двух требуемых мне моделей
class Case(models.Model):
    pass


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
