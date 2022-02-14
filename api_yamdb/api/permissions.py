from rest_framework import permissions, status
from rest_framework.exceptions import APIException

from users.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class OwnerOrHasRights(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author
                or request.user.role == User.ADMIN
                or request.user.role == User.MODERATOR)


class MethodNotAllowedException(APIException):
    """Method not allowed exception."""
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_code = 'Method now allowed'


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права доступа для жанров и категорий."""
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.user.is_authenticated:
            if request.method in ('POST', 'DELETE'):
                return request.user.role == User.ADMIN
            raise MethodNotAllowedException


class IsAdminOrReadOnlyTitles(permissions.BasePermission):
    """Права доступа для тайтлов."""
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.user.is_authenticated:
            if request.method in ('POST', 'PATCH', 'DELETE'):
                return request.user.role == User.ADMIN
            raise MethodNotAllowedException


class IsUserMethod(permissions.BasePermission):
    """Любой запрос кроме list недоступен."""
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.role == 'user'


class IsAdminMethod(permissions.BasePermission):
    """"Админу доступны 'create' и 'destroy'."""
    def has_permission(self, request, view):
        if request.method in ('DELETE', 'POST'):
            return request.user.role == User.ADMIN


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (bool(request.user and request.user.is_authenticated)
                and (request.user.role == User.ADMIN
                or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (bool(request.user and request.user.is_authenticated)
                and (request.user.role == User.ADMIN
                or request.user.is_superuser))
