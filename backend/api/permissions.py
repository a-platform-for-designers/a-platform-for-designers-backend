from rest_framework import permissions
from rest_framework.permissions import BasePermission


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


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'DELETE']:
            return obj.user == request.user
        return True
