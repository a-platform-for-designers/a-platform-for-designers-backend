from django.shortcuts import get_object_or_404
from rest_framework import permissions

from job.models import Chat


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права для администратора или только для чтения.

    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Права для автора или только для чтения.

    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'author'):
            author_field = 'author'
        elif hasattr(obj, 'customer'):
            author_field = 'customer'
        elif hasattr(obj, 'user'):
            author_field = 'user'
        else:
            return False
        return (
            request.method in permissions.SAFE_METHODS
            or getattr(obj, author_field) == request.user
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Права для владельца или только для чтения.

    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'DELETE']:
            return obj.user == request.user
        return True


class IsInitiatorOrReceiverChatPermission(permissions.BasePermission):
    """
    Права для работы с чатами.

    """

    def has_permission(self, request, view):
        if view.action == 'retrieve':
            chat_id = view.kwargs['pk']
            chat = get_object_or_404(Chat.objects.filter(pk=chat_id))
            return (
                chat.initiator == request.user or chat.receiver == request.user
            )
        else:
            return True

    def has_object_permission(self, request, view, obj):
        return obj.initiator == request.user or obj.receiver == request.user


class IsInitiatorOrReceiverMessagePermission(permissions.BasePermission):
    """
    Права для работы с сообщениями чатов.

    """

    def has_permission(self, request, view):
        chat_id = view.kwargs['chat_id']
        chat = get_object_or_404(Chat.objects.filter(pk=chat_id))
        return chat.initiator == request.user or chat.receiver == request.user

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.sender == request.user
        return (obj.chat.initiator == request.user
                or obj.chat.receiver == request.user)
