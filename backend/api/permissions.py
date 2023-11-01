from rest_framework import permissions
from rest_framework.permissions import BasePermission


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
        return obj.author == request.user


class IsOwnerOrReadOnly(BasePermission):
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

    def has_object_permission(self, request, view, obj):
        return obj.initiator == request.user or obj.receiver == request.user


class IsInitiatorOrReceiverMessagePermission(permissions.BasePermission):
    """
    Права для работы с сообщениями чатов.

    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.sender == request.user
        return (obj.chat.initiator == request.user
                or obj.chat.receiver == request.user)
