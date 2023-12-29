from rest_framework.response import Response


class CustomRetrieveMixin:
    """
    Кастомный миксин для обработки GET запроса для пользователя по ID.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
