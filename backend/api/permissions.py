from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsInitiatorOrReceiverChatPermission(permissions.BasePermission):
    """Права для работы с чатами."""

    def has_object_permission(self, request, view, obj):
        return obj.initiator == request.user or obj.receiver == request.user


class IsInitiatorOrReceiverMessagePermission(permissions.BasePermission):
    """Права для работы с сообщениями чатов."""

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.sender == request.user
        return (obj.chat.initiator == request.user
                or obj.chat.receiver == request.user)
