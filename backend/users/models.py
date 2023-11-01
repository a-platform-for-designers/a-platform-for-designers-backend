from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Класс UserManager для управления
    созданием и обработкой пользователей.

    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Требуется Email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.

    """
    date_joined = models.DateTimeField(
        auto_now_add=True
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=70,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=40,
        blank=False,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=40,
        blank=False,
    )
    photo = models.ImageField(
        'Фото',
        upload_to='avatars/',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True
    )
    is_customer = models.BooleanField(
        'Покупатель',
        default=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'


class ProfileCustomer(models.Model):
    """
    Модель профиля покупателя.

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']
        verbose_name = 'Профиль покупателя'
        verbose_name_plural = 'Профили покупателей'

    def __str__(self):
        return self.user.email


class ProfileDesigner(models.Model):
    """
    Модель профиля дизайнера.

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    specialization = models.IntegerField()
    hobby = models.CharField(max_length=255)
    language = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']
        verbose_name = 'Профиль дизайнера'
        verbose_name_plural = 'Профили дизайнеров'

    def __str__(self):
        return self.user.email


class Subscription(models.Model):
    """
    Модель, представляющая подписку между двумя пользователями.

    """

    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription'
            )
        ]

    def __str__(self):

        return f'{self.user.email} подписан на {self.author.email}'
