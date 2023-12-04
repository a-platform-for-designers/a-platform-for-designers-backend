from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django_countries.fields import CountryField
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
        extra_fields.setdefault('is_customer', False)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.

    """
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=70,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=40,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=40,
    )
    photo = models.ImageField(
        'Фото',
        upload_to='avatars/',
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(
        'Дата регистрации',
        auto_now_add=True
    )
    is_customer = models.BooleanField(
        'Покупатель',
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
    education = models.CharField(blank=True, null=True, max_length=50)
    country = CountryField(blank=True, null=True,)
    specialization = models.ManyToManyField(
        to='job.Specialization',
    )
    hobby = models.CharField(blank=True, null=True, max_length=200)
    language = models.ManyToManyField(
        to='job.Language',
        blank=True,
    )

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
