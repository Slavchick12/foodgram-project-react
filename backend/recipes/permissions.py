from rest_framework import permissions


class AuthorOrAdminOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method == 'POST' and request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user == obj.author
        )
