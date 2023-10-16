from django.contrib.auth import get_user_model
from djoser.views import UserViewSet


User = get_user_model()


class UserProfileViewSet(UserViewSet):
    """"
    Класс UserProfileViewSet для работы с профилями пользователей.

    """
    pass
